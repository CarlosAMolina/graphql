import datetime
import unittest


from src import database
from src.schema import schema


class TestEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()

    def test_all_users(self):
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
        result_nodes = [edge["node"] for edge in result.data["allUsers"]["edges"]]
        self.assertEqual(4, len(result_nodes))
        for user_data in database.users_data:
            for column_name, value in user_data.items():
                if column_name == "id":
                    continue
                else:
                    # TODO search how to request `creation_date_time` instead of `creationDateTime`.
                    if column_name == "creation_date_time":
                        column_name = "creationDateTime"
                        result_values = [
                            datetime.datetime.strptime(str(node.get(column_name)), "%Y-%m-%dT%H:%M:%S")
                            for node in result_nodes
                        ]
                    else:
                        result_values = [node.get(column_name) for node in result_nodes]
                    self.assertTrue(value in result_values)
