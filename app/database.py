import random
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_name = "database"
db_user = "user"
db_pass = "pass"
db_host = "localhost"
db_port = "5432"

db_string = "postgresql://{}:{}@{}:{}/{}".format(
    db_user, db_pass, db_host, db_port, db_name
)
engine = create_engine(db_string)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# def add_new_row(n):
#     with engine.connect() as connection:
#         connection.execute(text("INSERT INTO tasks (id,name,description) " +
#                 "VALUES (" +
#                 str(n) + ",'Hello','World')"))

#         connection.commit()

# if __name__ == '__main__':
#     print('Application started')
#     counter = 0

#     while counter < 1:
#         add_new_row(random.randint(1,1000))
#         print('Added new row')
#         counter += 1
