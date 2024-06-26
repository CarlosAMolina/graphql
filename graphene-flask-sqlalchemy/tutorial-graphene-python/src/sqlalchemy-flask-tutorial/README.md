## Steps to work with this project

Install `requirements.txt`.

Run the API:

```bash
cd src
python app.py
```

## Endpoints

- `allDepartments`. GraphQL body example in this [file](bruno/graphql/allDepartments.bru).
- `allEmployees`. GraphQL body example in this [file](bruno/graphql/allEmployees.bru).
- `search`. GraphQL body example in this [file](bruno/graphql/search.bru). [Search all Models with Union tutorial](https://docs.graphene-python.org/projects/sqlalchemy/en/latest/examples/).

### Different ways to request data

You can request data in multiple ways:

- Using [Bruno](https://www.usebruno.com/):
  - In the Bruno GUI, select `Import Collection > Bruno Collection` and select the `bruno/graphql.json` file. When asking for the location, select the same `bruno` folder where the `graphql.json` file is.
  - Copy the environment files to the new `graphql` folder that has been created: `cp -r environments/ graphql`.

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
