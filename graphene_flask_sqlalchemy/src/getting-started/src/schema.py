import graphene
import sqlalchemy as sa
from graphene_sqlalchemy import SQLAlchemyObjectType

import models


class ActiveSQLAlchemyObjectType(SQLAlchemyObjectType):
    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, info, id):
        return cls.get_query(info).filter(sa.and_(cls._meta.model.deleted_at is None, cls._meta.model.id == id)).first()


class User(ActiveSQLAlchemyObjectType):
    class Meta:
        model = models.UserModel
        # use `only_fields` to only expose specific fields ie "name"
        # only_fields = ("name",)
        # use `exclude_fields` to exclude specific fields ie "last_name"
        # exclude_fields = ("last_name",)


class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        query = User.get_query(info)  # SQLAlchemy query
        return query.all()


schema = graphene.Schema(query=Query)
