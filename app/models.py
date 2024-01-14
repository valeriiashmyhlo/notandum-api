import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, Unicode
from sqlalchemy.orm import relationship
from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    records = relationship(
        "Record", back_populates="task", cascade="all, delete-orphan"
    )


class Record(Base):
    __tablename__ = "records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Unicode(200), index=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), index=True)

    task = relationship("Task", back_populates="records", lazy="joined", innerjoin=True)
