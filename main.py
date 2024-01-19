from typing import Generic, List, TypeVar

from fastapi import Depends, FastAPI, File, Form, UploadFile
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


class BaseRecord(BaseModel):
    content: str


class Record(BaseModel):
    id: UUID4
    content: str
    task_id: UUID4


class TaskNew(BaseModel):
    name: str
    description: str


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


@app.delete("/task/{id}")
async def get_task(id: UUID4, connection: Session = Depends(get_db)):
    return db.delete_task(db=connection, task_id=id)


@app.post("/task/create")
async def create_task(
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    connection: Session = Depends(get_db),
):
    records = list(filter(None, (await file.read()).decode("utf-8").split("\n")))
    new_task = db.create_new_task(
        db=connection,
        task=schemas.TaskBase(name=name, description=description),
    )
    for record in records:
        record_parsed = BaseRecord.model_validate_json(record)
        db.create_new_record(
            db=connection,
            record=schemas.RecordBase(
                content=record_parsed.content, task_id=new_task.id
            ),
        )
    return "success"


@app.put("/task/{id}/update", response_model=Task)
async def update_task(id: UUID4, task: TaskNew, connection: Session = Depends(get_db)):
    updated_task = db.update_task(
        db=connection,
        task=schemas.Task(id=id, name=task.name, description=task.description),
    )
    return updated_task


class UploadedRecord(BaseModel):
    content: str


@app.post("/upload")
async def upload_record(file: UploadFile):
    records = await file.read()
    print(records)
    return {"filename": file.filename}
