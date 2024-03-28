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
