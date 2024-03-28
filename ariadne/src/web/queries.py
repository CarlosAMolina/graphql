import datetime
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


@query.field("numericAggregatePeople")
def resolve_numeric_aggregate_people(*_, function, field: str) -> tp.Optional[tp.Union[int, float]]:
    """
    Examples of aggregation in GraphQL:
    https://dgraph.io/docs/graphql/queries/aggregate/
    https://developer.salesforce.com/docs/platform/graphql/guide/aggregate-examples.html
    """
    field_values = [person[field] for person in data.people if person.get(field) is not None]
    if len(field_values) == 0:
        return None
    elif _are_all_values_int(field_values):
        if function == "avg":
            return sum(field_values) / len(field_values)
        elif function == "max":
            return max(field_values)
        elif function == "min":
            return min(field_values)
        elif function == "sum":
            return sum(field_values)
        else:
            raise ValueError
    else:
        raise TypeError(f"Field {field} values must be numeric")


@query.field("dateTimeAggregatePeople")
def resolve_date_time_aggregate_people(*_, function, field: str) -> tp.Optional[datetime.datetime]:
    field_values = [person[field] for person in data.people if person.get(field) is not None]
    if len(field_values) == 0:
        return None
    elif _are_all_values_date_time(field_values):
        if function == "max":
            return max(field_values)
        elif function == "min":
            return min(field_values)
        else:
            raise ValueError
    else:
        raise TypeError(f"Field {field} values must be date times")


def _are_all_values_int(array):
    return all(isinstance(value, numbers.Number) for value in array)


def _are_all_values_date_time(array):
    return all(isinstance(value, datetime.datetime) for value in array)
