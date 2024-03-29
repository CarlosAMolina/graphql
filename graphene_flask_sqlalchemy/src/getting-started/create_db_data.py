import pathlib

import db_session
import models


def run():
    if _exists_db_file():
        print("DB already exists")
    else:
        print("Start creating DB")
        _insert_db_data()


def _exists_db_file() -> bool:
    return pathlib.Path(db_session.db_file_name).is_file()


def _insert_db_data():
    models.Base.metadata.create_all(bind=db_session.engine)
    users = [
        models.UserModel(name="Peter", last_name="Red"),
        models.UserModel(name="Roy", last_name="Green"),
        models.UserModel(name="Tracy", last_name="Blue"),
    ]
    for row in users:
        db_session.db_session.add(row)
    db_session.db_session.commit()
