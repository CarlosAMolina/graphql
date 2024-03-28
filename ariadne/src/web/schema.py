from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query


schema_str = (Path(__file__).parent / "schema.graphql").read_text()
blindable_objects = [
    query,
]
schema = make_executable_schema(schema_str, blindable_objects)
