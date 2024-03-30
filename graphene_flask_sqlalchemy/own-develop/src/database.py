from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import datetime
import pathlib
import sqlalchemy as sa

import models


db_file_name = "database.sqlite3"
engine = sa.create_engine(f"sqlite:///{db_file_name}")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    if _exists_db_file():
        print("DB already exists")
    else:
        print("Start creating DB")
        _insert_db_data()


def _exists_db_file() -> bool:
    return pathlib.Path(db_file_name).is_file()


def _insert_db_data():
    models.Base.metadata.create_all(bind=engine)
    users_data = [
        {
            "id": 1,
            "name": "John",
            "age": 20,
            "creation_date_time": datetime.datetime(2024, 3, 20, 17, 20, 40),
        },
        {
            "id": 2,
            "name": "Jane",
            "age": 21,
            "creation_date_time": datetime.datetime(2023, 6, 17, 8, 15, 23),
        },
        {
            "id": 3,
            "name": "Al",
            "creation_date_time": datetime.datetime(2024, 10, 5, 8, 20, 23),
        },
        {
            "id": 4,
            "name": "Nick",
            "age": 41,
            "creation_date_time": datetime.datetime(2020, 12, 20, 20, 15, 42),
        },
    ]
    users = [
        models.UserModel(
            id=user_data["id"],
            name=user_data["name"],
            age=user_data.get("age"),
            creation_date_time=user_data["creation_date_time"],
        )
        for user_data in users_data
    ]
    for row in users:
        db_session.add(row)
    db_session.commit()
