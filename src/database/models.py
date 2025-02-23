from datetime import datetime
from typing import Literal

from sqlalchemy.sql.annotation import Annotated
from sqlmodel import SQLModel, Field

from src.database.session_manager import SessionManager


class ProjectBaseModel(SQLModel):
    pass


class PredictedFiles(ProjectBaseModel, table=True):
    __tablename__ = "predicted_files"
    file_name: str = Field(primary_key=True, index=True)
    created_at: datetime = Field(nullable=False)
    completed_at: datetime = Field(nullable=True, index=True)


class Predictions(ProjectBaseModel, table=True):
    __tablename__ = "predictions"
    file_name: str = Field(primary_key=True, index=True)
    total_bill: float = Field(nullable=False)
    sex: str = Field(nullable=False)
    smoker: str = Field(nullable=False)
    day: str = Field(nullable=False)
    time: str = Field(nullable=False)
    size: int = Field(nullable=False)
    tip: float = Field(nullable=False)
    created_at: datetime = Field(nullable=False)


def get_engine():
    session_manager = SessionManager()
    return session_manager.engine


def create_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
