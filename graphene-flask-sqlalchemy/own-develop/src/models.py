import database
import typing as tp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
import sqlalchemy as sa


Base = declarative_base()
# We will need this for querying
# https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/
Base.query = database.db_session.query_property()


class UserModel(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    age = sa.Column(sa.Integer)
    creation_date_time = sa.Column(sa.DateTime, nullable=False)
    country = sa.Column(sa.String)

    @hybrid_property
    def is_adult(self) -> tp.Optional[bool]:
        if self.age is None:
            return None
        else:
            return self.age > 18
