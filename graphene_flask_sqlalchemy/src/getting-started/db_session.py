import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker


db_file_name = "database.sqlite3"
engine = sa.create_engine(f"sqlite:///{db_file_name}")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
