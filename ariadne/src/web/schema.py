from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query
from web import types as custom_types


schema_str = (Path(__file__).parent / "schema.graphql").read_text()
blindable_objects = [
    custom_types.datetime_scalar,
    query,
]
schema = make_executable_schema(schema_str, blindable_objects)
