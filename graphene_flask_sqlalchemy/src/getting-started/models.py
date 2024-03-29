import sqlalchemy as sa
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_file_name = "database.sqlite3"
engine = sa.create_engine(f"sqlite:///{db_file_name}")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
