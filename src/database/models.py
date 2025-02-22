from datetime import datetime

from sqlmodel import SQLModel, Field

from src.database.session_manager import SessionManager
from src.utils.date_time_manager import DateTimeManager


class ProjectBaseModel(SQLModel):
    pass


class PredictedFiles(ProjectBaseModel, table=True):
    __tablename__ = "predicted_files"
    file_name: str = Field(primary_key=True, index=True)
    created_at: datetime = Field(
        default_factory=DateTimeManager.get_current_utc_time, nullable=False
    )
    completed_at: datetime = Field(nullable=True, index=True)


def get_engine():
    session_manager = SessionManager()
    return session_manager.engine


def create_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
