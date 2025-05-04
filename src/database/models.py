from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from src.database.session_manager import SessionManager


class ProjectBaseModel(SQLModel):
    pass


class Predictions(ProjectBaseModel, table=True):
    __tablename__ = "predictions"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    file_path: str = Field(nullable=True, index=True)
    total_bill: float = Field(nullable=False)
    sex: str = Field(nullable=False)
    smoker: str = Field(nullable=False)
    day: str = Field(nullable=False)
    time: str = Field(nullable=False)
    size: int = Field(nullable=False)
    tip: float = Field(nullable=False)
    real_tip: float = Field(nullable=False)
    prediction_source: str = Field(nullable=False)
    predicted_at: datetime = Field(nullable=False, index=True)


class TrainingData(ProjectBaseModel, table=True):
    __tablename__ = "training_data"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    total_bill: float = Field(nullable=False)
    sex: int = Field(nullable=False)
    smoker: int = Field(nullable=False)
    day: int = Field(nullable=False)
    time: int = Field(nullable=False)
    size: int = Field(nullable=False)
    tip: float = Field(nullable=False)
    trained_at: datetime = Field(nullable=False, index=True)


class DataIssues(ProjectBaseModel, table=True):
    __tablename__ = "data_issues"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    file_path: str = Field(nullable=False, index=True)
    evaluated_expectations: int = Field(nullable=True)
    successful_expectations: int = Field(nullable=True)
    unsuccessful_expectations: int = Field(nullable=True)
    success_percent: float = Field(nullable=True)
    missing_columns: int = Field(nullable=True)
    missing_values: int = Field(nullable=True)
    duplicated_rows: int = Field(nullable=True)
    unknown_categorical_values: int = Field(nullable=True)
    unknon_numeric_values: int = Field(nullable=True)
    bad_csv_encoding: int = Field(nullable=True)
    bad_csv_format: int = Field(nullable=True)
    other_parse_issues: int = Field(nullable=True)
    total_rows: int = Field(nullable=True)
    total_bad_rows: int = Field(nullable=True)
    created_at: datetime = Field(nullable=False, index=True)


def get_engine():
    session_manager = SessionManager()
    return session_manager.engine


def create_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
