import uuid
from sqlalchemy.orm import Session, joinedload
from . import models, schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: uuid.UUID):
    task = (
        db.query(models.Task)
        .options(joinedload(models.Task.records))
        .filter(models.Task.id == task_id)
        .first()
    )
    return task


def delete_task(db: Session, task_id: uuid.UUID):
    task = db.query(models.Task).filter(models.Task.id == task_id).delete()
    return task


def create_new_task(db: Session, task: schemas.TaskBase):
    db_task = models.Task(**task.model_dump(), id=uuid.uuid4())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def create_new_record(db: Session, record: schemas.RecordBase):
    db_record = models.Record(**record.model_dump(), id=uuid.uuid4())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
