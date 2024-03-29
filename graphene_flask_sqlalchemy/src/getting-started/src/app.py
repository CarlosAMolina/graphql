import database
from schema import schema


query = """
    query {
      users {
        name,
        lastName
      }
    }
"""

database.init_db()
result = schema.execute(query, context_value={"session": database.db_session})
print(result)
