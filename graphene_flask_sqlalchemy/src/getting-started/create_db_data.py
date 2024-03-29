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
    users = [
        models.UserModel(name="Peter", last_name="Red"),
        models.UserModel(name="Roy", last_name="Green"),
        models.UserModel(name="Tracy", last_name="Blue"),
    ]
    for row in users:
        models.db_session.add(row)
    models.db_session.commit()
