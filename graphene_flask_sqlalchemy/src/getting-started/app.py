from db_session import db_session
from schema import schema
import create_db_data


query = """
    query {
      users {
        name,
        lastName
      }
    }
"""

create_db_data.run()
result = schema.execute(query, context_value={"session": db_session})
print(result)
