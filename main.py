from typing import Generic, List, TypeVar

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import UUID4, BaseModel
from app import models, schemas, db
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic.generics import GenericModel


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ResponsePayload = TypeVar("ResponsePayload")


class Record(BaseModel):
    id: UUID4
    content: str
    task_id: UUID4


class TaskNew(BaseModel):
    name: str
    description: str
    records: List[str]


class Task(TaskNew):
    id: UUID4
    records: List[Record]


class Response(GenericModel, Generic[ResponsePayload]):
    data: List[ResponsePayload]


@app.get("/task/list", response_model=Response[Task])
async def get_task_list(
    skip: int = 0, limit: int = 100, connection: Session = Depends(get_db)
):
    tasks = db.get_tasks(db=connection, skip=skip, limit=limit)
    return Response(data=tasks)


@app.get("/task/{id}", response_model=Task)
async def get_task(id: UUID4, connection: Session = Depends(get_db)):
    return db.get_task(db=connection, task_id=id)


@app.delete("/task/{id}", response_model=Task)
async def get_task(id: UUID4, connection: Session = Depends(get_db)):
    return db.delete_task(db=connection, task_id=id)


@app.put("/task/create")
async def create_task(task: TaskNew, connection: Session = Depends(get_db)):
    new_task = db.create_new_task(
        db=connection,
        task=schemas.TaskBase(name=task.name, description=task.description),
    )
    for record in task.records:
        db.create_new_record(
            db=connection,
            record=schemas.RecordBase(content=record, task_id=new_task.id),
        )
    return "success"
