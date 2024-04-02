from flask import Flask
from flask_graphql import GraphQLView

from schema import schema
import database

app = Flask(__name__)
app.debug = True

URL_PATH_GRAPHQL = "graphql"

app.add_url_rule(
    f"/{URL_PATH_GRAPHQL}",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),  # for having the GraphiQL interface
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


if __name__ == "__main__":
    database.init_db()
    print("Start run server")
    print(f"GraphiQL URL: http://127.0.0.1:5000/{URL_PATH_GRAPHQL}")
    app.run()
