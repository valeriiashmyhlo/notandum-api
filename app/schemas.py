from typing import List
from pydantic import UUID4, BaseModel


class RecordBase(BaseModel):
    content: str
    task_id: UUID4

    class Config:
        orm_mode = True


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: UUID4

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    name: str
    description: str
    records: List[Record] = []

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    content: str


class Task(TaskBase):
    id: UUID4

    class Config:
        orm_mode = True
