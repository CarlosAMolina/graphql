import numbers
import typing as tp

from ariadne import QueryType

from web import data


query = QueryType()


@query.field("people")
def resolve_people(*_, input=None) -> list:
    """
    input: PeopleFilter (see schema.graphql)
    """
    filtered = [person for person in data.people]
    if input is None:
        return filtered
    if input.get("maxAge") is not None:
        filtered = [person for person in filtered if person["age"] <= input["maxAge"]]
    if input.get("minAge") is not None:
        filtered = [person for person in filtered if person["age"] >= input["minAge"]]
    return filtered


@query.field("aggregatePeople")
def resolve_aggregate_people(*_, function, field: str) -> tp.Optional[int]:
    """
    Examples of aggregation in GraphQL:
    https://dgraph.io/docs/graphql/queries/aggregate/
    https://developer.salesforce.com/docs/platform/graphql/guide/aggregate-examples.html
    """
    if function == "max":
        ages = [person[field] for person in data.people if person.get(field) is not None]
        _assert_int_values(ages)
        return None if len(ages) == 0 else max(ages)


def _assert_int_values(array):
    if not all(isinstance(value, numbers.Number) for value in array):
        raise TypeError
