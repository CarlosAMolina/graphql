import pathlib

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

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
    users = [
        models.UserModel(name="Peter", last_name="Red"),
        models.UserModel(name="Roy", last_name="Green"),
        models.UserModel(name="Tracy", last_name="Blue"),
    ]
    for row in users:
        db_session.add(row)
    db_session.commit()
