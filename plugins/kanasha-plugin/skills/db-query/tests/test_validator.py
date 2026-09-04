import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db_query_validator import validate_query


DATABASE = {
    "allowed_relations": ["public.example_safe_view"],
    "allowed_functions": [],
    "max_rows": 100,
}


class ValidatorTest(unittest.TestCase):
    def test_accepts_an_explicit_parameterized_select(self) -> None:
        result = validate_query(
            "SELECT id, created_at FROM public.example_safe_view WHERE application_id = $1 LIMIT 10",
            ["00000000-0000-0000-0000-000000000000"],
            DATABASE,
        )

        self.assertEqual(result["parameter_count"], 1)
        self.assertNotIn("00000000", result["audit_summary"])

    def test_rejects_writing_or_evasive_queries(self) -> None:
        forbidden_queries = (
            "INSERT INTO public.example_safe_view (id) VALUES ($1)",
            "UPDATE public.example_safe_view SET id = $1",
            "DELETE FROM public.example_safe_view",
            "CREATE TABLE public.temporary_result (id uuid)",
            "ALTER TABLE public.example_safe_view ADD COLUMN forbidden_column text",
            "DROP TABLE public.example_safe_view",
            "TRUNCATE TABLE public.example_safe_view",
            "COPY public.example_safe_view TO STDOUT",
            "CALL public.maintenance_procedure()",
            "WITH removed AS (DELETE FROM public.example_safe_view RETURNING id) SELECT id FROM removed",
            "SELECT id FROM public.example_safe_view; SELECT id FROM public.example_safe_view",
            "SELECT * FROM public.example_safe_view",
            "SELECT id INTO temporary_result FROM public.example_safe_view",
            "SELECT id FROM private.other_view",
            "SELECT pg_read_file($1) FROM public.example_safe_view",
            "SELECT pg_sleep($1) FROM public.example_safe_view",
        )

        for query in forbidden_queries:
            with self.subTest(query=query):
                with self.assertRaises(ValueError):
                    validate_query(query, ["value"], DATABASE)

    def test_rejects_missing_or_extra_parameters(self) -> None:
        query = "SELECT id FROM public.example_safe_view WHERE application_id = $1 LIMIT 10"

        with self.assertRaisesRegex(ValueError, "params_invalidos"):
            validate_query(query, [], DATABASE)
        with self.assertRaisesRegex(ValueError, "params_invalidos"):
            validate_query("SELECT id FROM public.example_safe_view LIMIT 10", ["extra"], DATABASE)

    def test_rejects_inline_values_outside_the_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "valor_literal_nao_permitido"):
            validate_query(
                "SELECT id FROM public.example_safe_view WHERE cd_status = 'ACTIVE' LIMIT 10",
                [],
                DATABASE,
            )

    def test_requires_a_literal_limit_within_the_alias_cap(self) -> None:
        with self.assertRaisesRegex(ValueError, "limit_obrigatorio"):
            validate_query("SELECT id FROM public.example_safe_view", [], DATABASE)
        with self.assertRaisesRegex(ValueError, "limit_nao_autorizado"):
            validate_query("SELECT id FROM public.example_safe_view LIMIT 101", [], {**DATABASE, "max_rows": 100})
