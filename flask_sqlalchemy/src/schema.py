import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Department as DepartmentModel, Employee as EmployeeModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node,)


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)


class SearchResult(graphene.Union):
    class Meta:
        types = (Department, Employee)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # `search` needs `resolve_search`
    search = graphene.List(SearchResult, q=graphene.String())  # List field for search results

    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(Employee.connection)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(Department.connection, sort=None)

    def resolve_search(self, info, **args):
        """
        https://docs.graphene-python.org/projects/sqlalchemy/en/latest/examples/
        """
        q = args.get("q")  # Search query
        department_query = Department.get_query(info)
        employee_query = Employee.get_query(info)
        departments = department_query.filter((DepartmentModel.name.contains(q))).all()
        employees = employee_query.filter((EmployeeModel.name.contains(q))).all()
        return departments + employees  # Combine lists


schema = graphene.Schema(query=Query)
