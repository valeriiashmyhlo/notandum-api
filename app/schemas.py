from typing import List
from pydantic import UUID4, BaseModel


class LabelCreate(BaseModel):
    content: str
    record_id: UUID4

    class Config:
        orm_mode = True


class Label(BaseModel):
    id: UUID4
    content: str
    record_id: UUID4

    class Config:
        orm_mode = True


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
    total_records: int = 0
    total_labels: int = 0

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    content: str


class Task(TaskBase):
    id: UUID4

    class Config:
        orm_mode = True
