from graphene import ObjectType
from graphene import relay
from graphene import Schema
from graphene import String
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType

import models


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.UserModel
        # Required by SQLAlchemyConnectionField.
        # https://docs.graphene-python.org/projects/sqlalchemy/en/latest/relay/
        # https://docs.graphene-python.org/en/latest/relay/nodes/
        interfaces = (relay.Node,)


class Query(ObjectType):
    # I think it can be commented.
    # https://docs.graphene-python.org/en/latest/relay/nodes/#node-root-field
    node = relay.Node.Field()
    # this defines a Field `hello` in our Schema with a single Argument `first_name`
    # By default, the argument name will automatically be camel-based into firstName in the generated schema
    hello = String(first_name=String(default_value="stranger"))
    goodbye = String()
    # Gives access to relay pagination, sorting and filtering.
    # I think that it avoid us to create a resolve function.
    # https://docs.graphene-python.org/projects/sqlalchemy/en/latest/relay/
    # Sort query example:
    # https://github.com/graphql-python/graphene-sqlalchemy/blob/master/examples/flask_sqlalchemy/app.py
    all_users = SQLAlchemyConnectionField(User.connection)

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (first_name) for the Field and returns data for the query Response
    def resolve_hello(root, info, first_name) -> str:
        return f"Hello {first_name}!"

    def resolve_goodbye(root, info) -> str:
        return "See ya!"


schema = Schema(query=Query)


if __name__ == "__main__":
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
