from flask import Flask
from flask_graphql import GraphQLView

from schema import schema
import database

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),  # for having the GraphiQL interface
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


# TODO move to test folder
def test_all_users():
    query = """
        {
          allUsers {
            edges {
              node {
                id,
                name,
                age,
                creationDateTime
              }
            }
          }
        }
    """
    result = schema.execute(query, context_value={"session": database.db_session})
    print(result)


if __name__ == "__main__":
    database.init_db()
    print("Start run server")
    # TODO UNCOMMENT app.run()
    test_all_users()
