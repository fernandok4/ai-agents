import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db_query_config import get_relation, public_databases, validate_config


def sample_document() -> dict[str, object]:
    return {
        "databases": {
            "example_postgres": {
                "enabled": True,
                "type": "postgresql",
                "host": "postgres.example.invalid",
                "port": 5432,
                "database": "example_database",
                "username": "reader",
                "password": "not-a-real-secret",
                "allowed_schemas": ["public"],
                "allowed_relations": ["public.example_safe_view"],
            }
        }
    }


class ConfigTest(unittest.TestCase):
    def test_normalizes_a_postgresql_alias_without_exposing_connection_fields(self) -> None:
        databases = validate_config(sample_document())

        self.assertEqual(public_databases(databases), [{"alias": "example_postgres", "type": "postgresql", "description": ""}])
        self.assertEqual(get_relation(databases["example_postgres"], "public.example_safe_view"), ("public", "example_safe_view"))

    def test_rejects_a_relation_outside_the_allowed_schema(self) -> None:
        document = sample_document()
        document["databases"]["example_postgres"]["allowed_relations"] = ["private.example_safe_view"]

        with self.assertRaisesRegex(ValueError, "configuracao_invalida"):
            validate_config(document)

    def test_rejects_a_non_postgresql_database(self) -> None:
        document = sample_document()
        document["databases"]["example_postgres"]["type"] = "mysql"

        with self.assertRaisesRegex(ValueError, "configuracao_invalida"):
            validate_config(document)

    def test_disabled_alias_is_not_available_to_the_broker(self) -> None:
        document = sample_document()
        document["databases"]["example_postgres"]["enabled"] = False

        self.assertEqual(validate_config(document), {})
