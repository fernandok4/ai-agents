"""Leitura e validação da configuração privada do broker."""

import re
from pathlib import Path

import yaml


IDENTIFIER = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")
ALIAS = re.compile(r"^[a-z][a-z0-9_-]{0,62}$")
MAX_ROWS_CAP = 1_000


def load_config(config_path: str) -> dict[str, dict[str, object]]:
    try:
        with Path(config_path).open("r", encoding="utf-8") as config_file:
            document = yaml.safe_load(config_file)
    except (OSError, yaml.YAMLError) as error:
        raise ValueError("configuracao_invalida") from error
    return validate_config(document)


def validate_config(document: object) -> dict[str, dict[str, object]]:
    if not isinstance(document, dict) or set(document) != {"databases"}:
        raise ValueError("configuracao_invalida")
    raw_databases = document["databases"]
    if not isinstance(raw_databases, dict) or not raw_databases:
        raise ValueError("configuracao_invalida")

    databases: dict[str, dict[str, object]] = {}
    for alias, raw_database in raw_databases.items():
        if not isinstance(alias, str) or not ALIAS.fullmatch(alias):
            raise ValueError("configuracao_invalida")
        if not isinstance(raw_database, dict):
            raise ValueError("configuracao_invalida")
        if raw_database.get("enabled") is False:
            continue
        databases[alias] = normalize_database(raw_database)
    return databases


def normalize_database(raw_database: dict[object, object]) -> dict[str, object]:
    required_fields = ("host", "database", "username", "password", "allowed_schemas", "allowed_relations")
    if raw_database.get("type") != "postgresql" or raw_database.get("enabled") is not True:
        raise ValueError("configuracao_invalida")
    if any(not isinstance(raw_database.get(field), str) or not raw_database[field] for field in required_fields[:4]):
        raise ValueError("configuracao_invalida")

    schemas = normalize_identifiers(raw_database["allowed_schemas"])
    relations = normalize_relations(raw_database["allowed_relations"], schemas)
    functions = normalize_identifiers(raw_database.get("allowed_functions", []), allow_empty=True)
    description = raw_database.get("description", "")
    if not isinstance(description, str) or len(description) > 240:
        raise ValueError("configuracao_invalida")

    return {
        "type": "postgresql",
        "host": raw_database["host"],
        "port": normalize_integer(raw_database.get("port", 5432), 1, 65535),
        "database": raw_database["database"],
        "username": raw_database["username"],
        "password": raw_database["password"],
        "connect_timeout_seconds": normalize_integer(raw_database.get("connect_timeout_seconds", 5), 1, 60),
        "statement_timeout_ms": normalize_integer(raw_database.get("statement_timeout_ms", 10_000), 100, 60_000),
        "max_rows": normalize_integer(raw_database.get("max_rows", 100), 1, MAX_ROWS_CAP),
        "allowed_schemas": schemas,
        "allowed_relations": relations,
        "allowed_functions": functions,
        "description": description,
    }


def normalize_integer(value: object, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum or value > maximum:
        raise ValueError("configuracao_invalida")
    return value


def normalize_identifiers(value: object, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ValueError("configuracao_invalida")
    normalized = []
    for identifier in value:
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            raise ValueError("configuracao_invalida")
        normalized.append(identifier)
    return sorted(set(normalized))


def normalize_relations(value: object, schemas: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("configuracao_invalida")
    normalized = []
    for relation in value:
        if not isinstance(relation, str):
            raise ValueError("configuracao_invalida")
        parts = relation.split(".")
        if len(parts) != 2 or not all(IDENTIFIER.fullmatch(part) for part in parts):
            raise ValueError("configuracao_invalida")
        if parts[0] not in schemas:
            raise ValueError("configuracao_invalida")
        normalized.append(relation)
    return sorted(set(normalized))


def get_database(databases: dict[str, dict[str, object]], alias: object) -> dict[str, object]:
    if not isinstance(alias, str) or alias not in databases:
        raise ValueError("banco_nao_autorizado")
    return databases[alias]


def get_relation(database: dict[str, object], reference: object) -> tuple[str, str]:
    if not isinstance(reference, str) or reference not in database["allowed_relations"]:
        raise ValueError("relacao_nao_autorizada")
    return tuple(reference.split(".", maxsplit=1))


def public_databases(databases: dict[str, dict[str, object]]) -> list[dict[str, str]]:
    return [
        {
            "alias": alias,
            "type": "postgresql",
            "description": str(database["description"]),
        }
        for alias, database in sorted(databases.items())
    ]
