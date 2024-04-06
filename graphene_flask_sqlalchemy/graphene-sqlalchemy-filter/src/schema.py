from graphene import Connection
from graphene import Node
from graphene import ObjectType
from graphene import Schema
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField
from graphene_sqlalchemy_filter import FilterSet
import graphene

import models


# `Quick start` tutorial section.
class UserFilter(FilterSet):
    is_john = graphene.Boolean()

    class Meta:
        model = models.UserModel
        fields = {
            "name": ["in"],
        }

    @staticmethod
    def is_john_filter(info, query, value):
        desired_name = "John"
        if value:
            return models.UserModel.name == desired_name
        else:
            return models.UserModel.username != desired_name


# https://github.com/art1415926535/graphene-sqlalchemy-filter/blob/master/tests/graphql_objects.py
class MyFilterableConnectionField(FilterableConnectionField):
    filters = {
        models.UserModel: UserFilter(),
    }


class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = models.UserModel
        interfaces = (Node,)
        connection_field_factory = MyFilterableConnectionField.factory


class UserConnection(Connection):
    class Meta:
        node = UserNode


class Query(ObjectType):
    all_users = FilterableConnectionField(UserConnection, filters=UserFilter())


schema = Schema(query=Query)
