"""Validação estrutural de SQL PostgreSQL antes de chegar ao driver."""

import hashlib

import sqlglot
from sqlglot import exp


BLOCKED_EXPRESSION_NAMES = frozenset(
    {
        "Alter",
        "Analyze",
        "Attach",
        "Command",
        "Copy",
        "Create",
        "Delete",
        "Drop",
        "Grant",
        "Insert",
        "Lock",
        "Merge",
        "Pragma",
        "Revoke",
        "TruncateTable",
        "Update",
        "Use",
    }
)
SAFE_FUNCTIONS = frozenset(
    {
        "abs",
        "avg",
        "cast",
        "ceil",
        "coalesce",
        "concat",
        "count",
        "date_trunc",
        "extract",
        "floor",
        "greatest",
        "least",
        "length",
        "lower",
        "max",
        "min",
        "nullif",
        "round",
        "sum",
        "trim",
        "upper",
    }
)
DANGEROUS_FUNCTIONS = frozenset(
    {
        "current_setting",
        "dblink",
        "lo_export",
        "lo_import",
        "nextval",
        "pg_advisory_lock",
        "pg_advisory_xact_lock",
        "pg_cancel_backend",
        "pg_ls_dir",
        "pg_read_binary_file",
        "pg_read_file",
        "pg_sleep",
        "pg_stat_file",
        "pg_terminate_backend",
        "set_config",
        "setval",
    }
)


def validate_query(sql: object, params: object, database: dict[str, object]) -> dict[str, object]:
    if not isinstance(sql, str) or not sql.strip() or len(sql.encode("utf-8")) > 60_000:
        raise ValueError("consulta_invalida")
    if not isinstance(params, list) or not all(is_json_scalar(parameter) for parameter in params):
        raise ValueError("params_invalidos")

    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError as error:
        raise ValueError("consulta_invalida") from error
    if len(statements) != 1 or not isinstance(statements[0], exp.Select):
        raise ValueError("consulta_nao_permitida")

    expression = statements[0]
    reject_blocked_expressions(expression)
    reject_wildcard_projections(expression)
    relations = validate_relations(expression, database)
    functions = validate_functions(expression, database)
    parameter_count = validate_parameters(expression, params)
    validate_limit(expression, database)
    reject_inline_literals(expression)
    normalized = expression.sql(dialect="postgres")
    fingerprint = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return {
        "sql": sql,
        "parameter_count": parameter_count,
        "audit_summary": (
            f"statement=SELECT relations={','.join(relations)} "
            f"functions={','.join(functions) or 'none'} parameters={parameter_count} fingerprint={fingerprint}"
        ),
    }


def is_json_scalar(value: object) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def reject_blocked_expressions(expression: exp.Expression) -> None:
    for node in expression.walk():
        if type(node).__name__ in BLOCKED_EXPRESSION_NAMES:
            raise ValueError("consulta_nao_permitida")
    if any(select.args.get("into") is not None for select in expression.find_all(exp.Select)):
        raise ValueError("consulta_nao_permitida")


def reject_wildcard_projections(expression: exp.Expression) -> None:
    for select in expression.find_all(exp.Select):
        for projection in select.expressions:
            if any(isinstance(node, exp.Star) for node in projection.walk()):
                raise ValueError("wildcard_nao_permitido")


def validate_relations(expression: exp.Expression, database: dict[str, object]) -> list[str]:
    cte_names = {cte.alias_or_name.lower() for cte in expression.find_all(exp.CTE) if cte.alias_or_name}
    relations = []
    allowed_relations = set(database["allowed_relations"])
    for table in expression.find_all(exp.Table):
        table_name = table.name.lower()
        schema = table.db.lower() if table.db else ""
        if table_name in cte_names and not schema:
            continue
        if table.catalog or not schema:
            raise ValueError("relacao_nao_autorizada")
        relation = f"{schema}.{table_name}"
        if relation not in allowed_relations:
            raise ValueError("relacao_nao_autorizada")
        relations.append(relation)
    if not relations:
        raise ValueError("relacao_nao_autorizada")
    return sorted(set(relations))


def validate_functions(expression: exp.Expression, database: dict[str, object]) -> list[str]:
    allowed_functions = SAFE_FUNCTIONS | set(database["allowed_functions"])
    functions = []
    for function in expression.find_all(exp.Func):
        function_name = function.sql_name().lower()
        if function_name == "anonymous":
            function_name = function.name.lower()
        if function_name in DANGEROUS_FUNCTIONS or function_name not in allowed_functions:
            raise ValueError("funcao_nao_autorizada")
        functions.append(function_name)
    return sorted(set(functions))


def validate_parameters(expression: exp.Expression, params: list[object]) -> int:
    indexes = []
    for parameter in expression.find_all(exp.Parameter):
        try:
            indexes.append(int(parameter.name))
        except (TypeError, ValueError) as error:
            raise ValueError("params_invalidos") from error
    if not indexes:
        if params:
            raise ValueError("params_invalidos")
        return 0
    expected_indexes = list(range(1, max(indexes) + 1))
    if sorted(set(indexes)) != expected_indexes or len(params) != max(indexes):
        raise ValueError("params_invalidos")
    return len(params)


def validate_limit(expression: exp.Expression, database: dict[str, object]) -> None:
    limit = expression.args.get("limit")
    if not isinstance(limit, exp.Limit) or not isinstance(limit.expression, exp.Literal):
        raise ValueError("limit_obrigatorio")
    try:
        limit_value = int(limit.expression.this)
    except (TypeError, ValueError) as error:
        raise ValueError("limit_obrigatorio") from error
    if limit_value < 1 or limit_value > int(database["max_rows"]):
        raise ValueError("limit_nao_autorizado")


def reject_inline_literals(expression: exp.Expression) -> None:
    limit = expression.args["limit"]
    for literal in expression.find_all(exp.Literal):
        if literal is limit.expression or isinstance(literal.parent, exp.Parameter):
            continue
        else:
            raise ValueError("valor_literal_nao_permitido")
