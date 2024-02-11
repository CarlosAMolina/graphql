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

In the browser, open <http://localhost:5000/graphql>. And execute:

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

## Resources

Tutorial

<https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/>

- Fix tutorial errors

  <https://github.com/graphql-python/graphene-sqlalchemy/issues/272>
