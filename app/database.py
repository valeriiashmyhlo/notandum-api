from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_name = "database"
db_user = "user"
db_pass = "pass"
db_host = "localhost"
db_port = "5432"

db_sqlite_string = "sqlite:///db.sqlite".format(
    db_user, db_pass, db_host, db_port, db_name
)
db_string = "postgresql://{}:{}@{}:{}/{}".format(
    db_user, db_pass, db_host, db_port, db_name
)

engine = create_engine(db_sqlite_string)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(db_connection, connection_record):
    cursor = db_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
