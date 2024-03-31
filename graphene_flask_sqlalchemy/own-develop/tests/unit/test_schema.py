import unittest


from src import database
from src.schema import schema


class TestEndpoints(unittest.TestCase):
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
        database.init_db()
        result = schema.execute(query, context_value={"session": database.db_session})
        result_edges = result.data["allUsers"]["edges"]
        self.assertEqual(4, len(result_edges))
