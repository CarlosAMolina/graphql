import datetime
import typing as tp

from flask import g
from graphene import Int
from graphene import ObjectType
from graphene import relay
from graphene import Schema
from graphene import String
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.fields import default_connection_field_factory
from graphene_sqlalchemy_filter import FilterableConnectionField
from graphene_sqlalchemy_filter import FilterSet
from sqlalchemy.sql.expression import func
import graphene

import models


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.UserModel
        # Required by SQLAlchemyConnectionField.
        # https://docs.graphene-python.org/projects/sqlalchemy/en/latest/relay/
        # https://docs.graphene-python.org/en/latest/relay/nodes/
        interfaces = (relay.Node,)


# Implement filtering: https://jeffersonheard.github.io/python/graphql/2018/12/08/graphene-python.html
# I have modified the code in the previous URL to work with sort.
class UserConn(SQLAlchemyConnectionField):
    @classmethod
    def get_query(cls, model, info, **args):
        sort = args.pop("sort", None)
        query = super().get_query(model, info, sort, **args)
        if "country" in args:
            query = query.filter_by(country=args["country"])
        return query


class CountableConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    totalCount = graphene.Int()

    @staticmethod
    def resolve_totalCount(root, info, *args, **kwargs) -> int:
        query = g.custom_query
        result = query.count()
        return result


class AggregationConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    integer = graphene.Int()
    date_time = graphene.DateTime()

    @staticmethod
    def resolve_integer(root, info, *args, **kwargs) -> int:
        query = g.custom_query
        result = query.one()[0]
        return result

    @staticmethod
    def resolve_date_time(root, info, *args, **kwargs) -> datetime.datetime:
        query = g.custom_query
        result = query.one()[0]
        return result


class CountableSQLAlchemyObjectType(SQLAlchemyObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        model=None,
        registry=None,
        skip_registry=False,
        only_fields=(),
        exclude_fields=(),
        connection=None,
        connection_class=CountableConnection,
        use_connection=None,
        interfaces=(),
        id=None,
        connection_field_factory=default_connection_field_factory,  # TODO try not use default_connection_field_factory
        _meta=None,
        **options,
    ):
        super().__init_subclass_with_meta__(
            model,
            registry,
            skip_registry,
            only_fields,
            exclude_fields,
            connection,
            connection_class,
            use_connection,
            interfaces,
            id,
            connection_field_factory,
            _meta,
            **options,
        )


class AggregationSQLAlchemyObjectType(SQLAlchemyObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        **args,
    ):
        super().__init_subclass_with_meta__(
            **args,
            connection_class=AggregationConnection,
        )


class UserObj(CountableSQLAlchemyObjectType):
    class Meta:
        model = models.UserModel
        interfaces = (graphene.relay.Node,)


class UserAggregationObj(AggregationSQLAlchemyObjectType):
    class Meta:
        model = models.UserModel
        interfaces = (graphene.relay.Node,)


ALL_OPERATIONS = [
    "eq",
    "ne",
    "like",
    "ilike",
    "is_null",
    "in",
    "not_in",
    "lt",
    "lte",
    "gt",
    "gte",
    "range",
]


def get_filter_fields(model, operations=ALL_OPERATIONS):
    columns = get_columns_from_model(model)
    return {column: operations for column in columns}


def get_columns_from_model(model):
    return model().__table__.columns.keys()


class UserFilter(FilterSet):
    class Meta:
        model = models.UserModel
        fields = get_filter_fields(models.UserModel)


class PaginationFilterableConnectionField(FilterableConnectionField):
    def __init__(self, *args, **kwargs):
        self.kwargs = dict(**kwargs)
        if "connection" not in kwargs:
            raise ValueError("Connection must exists")
        kwargs["args"] = {
            "limit": graphene.Int(),
            "offset": graphene.Int(),
            "doquery": graphene.Boolean(),
            "group_by": graphene.List(graphene.String),
            "columns": graphene.List(graphene.String),
            "labels": graphene.List(graphene.String),
        }
        super().__init__(*args, **kwargs)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query_to_return = super().get_query(model, info, sort, **args)
        if "group_by" in args and args["group_by"] != []:
            query_to_return = cls._apply_group_by_query(cls, query_to_return, model, args["group_by"])
        query_to_return = cls._add_limit_and_offset_to_query(cls, query_to_return, **args)
        if "doquery" in args:
            g.custom_query = query_to_return
        return query_to_return if args.get("doquery", True) else []

    def _add_limit_and_offset_to_query(self, query, **args):
        if "limit" in args:
            query = query.limit(args["limit"])
        if "offset" in args:
            query = query.offset(args["offset"])
        return query

    def _apply_group_by_query(self, query, model, fields):
        model_fields = [getattr(model, item) for item in fields]
        query = query.group_by(*model_fields)
        return query


class AggregationFilterableConnectionField(FilterableConnectionField):
    def __init__(self, *args, **kwargs):
        self.kwargs = dict(**kwargs)
        if "connection" not in kwargs:
            raise ValueError("Connection must exists")
        kwargs["args"] = {
            "group_by": graphene.List(graphene.String),
            "aggregation_and_field": graphene.List(graphene.String),
        }
        super().__init__(*args, **kwargs)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query_to_return = super().get_query(model, info, sort, **args)

        if "group_by" in args and args["group_by"] != []:
            query_to_return = cls._apply_group_by_query(cls, query_to_return, model, args["group_by"])
        if "aggregation_and_field" in args and args["aggregation_and_field"] != []:
            query_to_return = cls._apply_aggregation(cls, query_to_return, model, args["aggregation_and_field"])
        g.custom_query = query_to_return
        return query_to_return

    def _apply_group_by_query(self, query, model, fields):
        model_fields = [getattr(model, item) for item in fields]
        query = query.group_by(*model_fields)
        return query

    def _apply_aggregation(self, query, model, aggregation_and_field: tp.List[str]):
        aggregation, field = aggregation_and_field[0], aggregation_and_field[1]
        entity = getattr(model, field)
        if aggregation == "max":
            return query.with_entities(func.max(entity))
        if aggregation == "min":
            return query.with_entities(func.min(entity))
        raise ValueError(aggregation)


class Query(ObjectType):
    # I think it can be commented.
    # https://docs.graphene-python.org/en/latest/relay/nodes/#node-root-field
    node = relay.Node.Field()
    # this defines a Field `hello` in our Schema with a single Argument `first_name`
    # By default, the argument name will automatically be camel-based into firstName in the generated schema
    hello = String(first_name=String(default_value="stranger"))
    goodbye = String()
    # Gives access to relay pagination and sorting.
    # I think that it avoid us to create a resolve function.
    # https://docs.graphene-python.org/projects/sqlalchemy/en/latest/relay/
    # Sort query example:
    # https://github.com/graphql-python/graphene-sqlalchemy/blob/master/examples/flask_sqlalchemy/app.py
    all_users = SQLAlchemyConnectionField(User.connection)
    all_users_filter = UserConn(
        User,
        args={
            "country": graphene.Argument(graphene.String),
            "sort": graphene.Argument(graphene.List(User.sort_enum())),
        },
    )
    """
    Examples of aggregation in GraphQL:
    https://dgraph.io/docs/graphql/queries/aggregate/
    https://developer.salesforce.com/docs/platform/graphql/guide/aggregate-examples.html
    """
    aggregate_users_int = Int(function_=String())
    pagination_users = PaginationFilterableConnectionField(
        connection=UserObj, filters=UserFilter(), sort=UserObj.sort_argument()
    )
    # TODO try apply filters
    aggregation_users = AggregationFilterableConnectionField(
        connection=UserAggregationObj, filters=UserFilter(), sort=None
    )

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (first_name) for the Field and returns data for the query Response
    def resolve_hello(root, info, first_name) -> str:
        return f"Hello {first_name}!"

    def resolve_goodbye(root, info) -> str:
        return "See ya!"

    def resolve_aggregate_users_int(root, info, function_) -> int:
        if function_ == "count":
            return 4  # TODO count db values
        raise ValueError(function_)


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
