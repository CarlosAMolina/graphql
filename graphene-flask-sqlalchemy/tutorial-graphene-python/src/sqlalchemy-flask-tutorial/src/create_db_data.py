import pathlib

import models


def run():
    if _exists_db_file():
        print("DB already exists")
    else:
        print("Start creating DB")
        _insert_db_data()


def _exists_db_file() -> bool:
    return pathlib.Path(models.db_file_name).is_file()


def _insert_db_data():
    models.Base.metadata.create_all(bind=models.engine)
    departments = {
        "engineering": models.Department(name="Engineering"),
        "hr": models.Department(name="Human Resources"),
    }
    employees = [
        models.Employee(name="Peter", department=departments["engineering"]),
        models.Employee(name="Roy", department=departments["engineering"]),
        models.Employee(name="Tracy", department=departments["hr"]),
    ]
    rows_to_insert = list(departments.values()) + employees
    for row in rows_to_insert:
        models.db_session.add(row)
    models.db_session.commit()
