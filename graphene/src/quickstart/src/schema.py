from graphene import ObjectType, String, Schema


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `first_name`
    # By default, the argument name will automatically be camel-based into firstName in the generated schema
    hello = String(first_name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (first_name) for the Field and returns data for the query Response
    def resolve_hello(root, info, first_name):
        return f"Hello {first_name}!"

    def resolve_goodbye(root, info):
        return "See ya!"


schema = Schema(query=Query)

# we can query for our field (with the default argument)
query_string = "{ hello }"
result = schema.execute(query_string)
print(result.data["hello"])
# "Hello stranger!"

# or passing the argument in the query
query_with_argument = '{ hello(firstName: "GraphQL") }'
result = schema.execute(query_with_argument)
print(result.data["hello"])
# "Hello GraphQL!"
