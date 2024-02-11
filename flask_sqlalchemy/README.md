## Steps to work with this project

Install `requirements.txt`.

Important. To run the api, work in the `src` folder:

```bash
cd src
```

If the `database.sqlite3` file does not exist, run:

```bash
# In the `src` folder.
python script_create_db_data.py
```

Run the API:

```bash
# In the `src` folder.
python app.py
```

You can request data in multiple ways:

- In the browser, open <http://localhost:5000/graphql>. And execute:

```
{
  allEmployees {
    edges {
      node {
        id
        name
        department {
          name
        }
      }
    }
  }
}
```

- Curl request. In a terminal:

  - POST request:

    ```bash
    curl 'http://127.0.0.1:5000/graphql?' -X POST -H 'Content-Type: application/json' --data-raw '{"query":"{\n  allEmployees {\n    edges {\n      node {\n        id\n        name\n        department {\n          name\n        }\n      }\n    }\n  }\n}"}'
    ```

  - GET request:

    ```bash
    curl http://127.0.0.1:5000/graphql?query=%7BallEmployees%7Bedges%7Bnode%7Bid%20name%20department%7Bname%7D%7D%7D%7D%7D
    ```

## Resources

Tutorial

<https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/>

- Fix tutorial errors

  <https://github.com/graphql-python/graphene-sqlalchemy/issues/272>
