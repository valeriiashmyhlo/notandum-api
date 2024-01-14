import random
from threading import Event, Thread
import time
from sqlalchemy import create_engine, text


db_name = 'database'
db_user = 'user'
db_pass = 'pass'
db_host = 'localhost'
db_port = '5432'

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def add_new_row(n):
    with db.connect() as connection:
        connection.execute(text("INSERT INTO tasks (id,name,description) " +
                "VALUES (" +
                str(n) + ",'Hello','World')"))
    
        connection.commit()

if __name__ == '__main__':
    print('Application started')
    counter = 0
    
    while counter < 1:
        add_new_row(random.randint(1,1000))
        print('Added new row')
        counter += 1

def get_task_list():
    with db.connect() as connection:
        result = connection.execute(text("SELECT * FROM tasks"))
        tasks = []
        for row in result:
            tasks.append({
                "id": row[0],
                "name": row[1],
                "description": row[2]
            })
        return tasks
