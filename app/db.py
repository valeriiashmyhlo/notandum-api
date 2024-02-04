import uuid
from sqlalchemy.orm import Session
from . import models, schemas


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: uuid.UUID):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    return task


def delete_task(db: Session, task_id: uuid.UUID):
    db.query(models.Task).filter(models.Task.id == task_id).delete()
    db.commit()
    return "deleted"


def update_task(db: Session, task: schemas.Task):
    db_task = db.query(models.Task).filter(models.Task.id == task.id).first()
    db_task.name = task.name
    db_task.description = task.description
    db.commit()
    return db_task


def create_new_task(db: Session, task: schemas.TaskBase):
    db_task = models.Task(
        **task.model_dump(),
        id=uuid.uuid4(),
    )
    db.add(db_task)
    db.commit()
    return db_task


def get_record(db: Session, id: uuid.UUID, skip: int = 0, limit: int = 100):
    return db.query(models.Record).filter(models.Record.id == id).first()


def get_records_labeled(
    db: Session, task_id: uuid.UUID, skip: int = 0, limit: int = 100
):
    query = db.query(models.Record).filter(models.Record.task_id == task_id)
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    return query.yield_per(1000)


def get_next_record_to_label(
    db: Session, task_id: uuid.UUID, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Record)
        .filter(models.Record.task_id == task_id)
        .filter(models.Record.status == None)
        .first()
    )


def set_next_record_id(db: Session, task_id: uuid.UUID):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    task.next_record_id = task.records[0].id
    db.commit()
    return task


def create_new_record(db: Session, record: schemas.RecordBase):
    db_record = models.Record(**record.model_dump(), id=uuid.uuid4())
    db.add(db_record)
    db.commit()
    return db_record


def create_new_label(db: Session, label: schemas.LabelCreate):
    db_label = models.Label(**label.model_dump(), id=uuid.uuid4())
    db.add(db_label)
    record = db.query(models.Record).filter(models.Record.id == label.record_id).first()
    record.status = "done"
    db.commit()

    task = db.query(models.Task).filter(models.Task.id == record.task_id).first()
    task.total_labels += 1
    next_record = get_next_record_to_label(db, task.id)
    if next_record is None:
        task.next_record_id = None
    else:
        task.next_record_id = next_record.id
    db.commit()
    return db_label
