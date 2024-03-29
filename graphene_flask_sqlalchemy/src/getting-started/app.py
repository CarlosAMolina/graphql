from schema import schema
import create_db_data
import models


query = """
    query {
      users {
        name,
        lastName
      }
    }
"""

create_db_data.run()
result = schema.execute(query, context_value={"session": models.db_session})
print(result)
