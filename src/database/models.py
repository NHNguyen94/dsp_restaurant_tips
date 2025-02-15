import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field

from src.utils.date_time_manager import DateTimeManager


class ProjectBaseModel(SQLModel):
    pass


class FileRegistration(ProjectBaseModel, table=True):
    __tablename__ = "file_registration"
    file_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    file_path: str = Field(max_length=255, nullable=False, unique=False)
    created_at: datetime = Field(
        default_factory=DateTimeManager.get_current_utc_time, nullable=False
    )
    completed_at: datetime = Field(nullable=True)


class DataIssues(ProjectBaseModel, table=True):
    __tablename__ = "data_issues"
    file_id: uuid.UUID = Field(
        foreign_key="file_registration.file_id", primary_key=True
    )
    row_missing: int = Field(nullable=False)
    rows_unknown_value: int = Field(nullable=False)
    rows_invalid_value: int = Field(nullable=False)
    rows_outlier: int = Field(nullable=False)
    features_missing: int = Field(nullable=False)
    label_missing: int = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=DateTimeManager.get_current_utc_time, nullable=False
    )
