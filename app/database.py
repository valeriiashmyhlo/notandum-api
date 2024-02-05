from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# db_string = "postgresql://{}:{}@{}:{}/{}".format(
#     db_user, db_pass, db_host, db_port, db_name
# )

engine = create_engine(os.environ["DATABASE_URL"])


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
