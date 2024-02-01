import uuid
from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship
from app.database import Base
import json


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    next_record_id = Column(UUID(as_uuid=True), index=True)
    total_records = Column(Integer, index=True)
    total_labels = Column(Integer, index=True)

    records = relationship(
        "Record",
        back_populates="task",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Unicode(500), index=True)
    status = Column(String, index=True)

    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), index=True
    )
    task = relationship(
        "Task",
        back_populates="records",
        lazy="joined",
        innerjoin=True,
    )

    labels = relationship(
        "Label",
        back_populates="record",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def serialize(self):
        return {
            "content": self.content,
            "labels": [json.loads(label.content) for label in self.labels],
        }


class Label(Base):
    __tablename__ = "labels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Unicode(500), index=True)

    record_id = Column(
        UUID(as_uuid=True), ForeignKey("records.id", ondelete="CASCADE"), index=True
    )
    record = relationship(
        "Record",
        back_populates="labels",
        lazy="joined",
        innerjoin=True,
    )
