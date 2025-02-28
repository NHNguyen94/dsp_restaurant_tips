from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from src.database.session_manager import SessionManager


class ProjectBaseModel(SQLModel):
    pass


class Predictions(ProjectBaseModel, table=True):
    __tablename__ = "predictions"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    file_path: str = Field(nullable=False, index=True)
    total_bill: float = Field(nullable=False)
    sex: str = Field(nullable=False)
    smoker: str = Field(nullable=False)
    day: str = Field(nullable=False)
    time: str = Field(nullable=False)
    size: int = Field(nullable=False)
    tip: float = Field(nullable=False)
    created_at: datetime = Field(nullable=False, index=True)


def get_engine():
    session_manager = SessionManager()
    return session_manager.engine


def create_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
