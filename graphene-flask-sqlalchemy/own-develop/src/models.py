from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

import database


Base = declarative_base()
# We will need this for querying
# https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
Base.query = database.db_session.query_property()


class UserModel(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    creation_date_time = sa.Column(sa.DateTime)
