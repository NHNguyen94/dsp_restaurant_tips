from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field

from src.database.session_manager import SessionManager


class ProjectBaseModel(SQLModel):
    pass


class Predictions(ProjectBaseModel, table=True):
    __tablename__ = "predictions"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    file_path: str = Field(nullable=False, index=True)
=======
    file_path: str = Field(nullable=True, index=True)
>>>>>>> main
=======
    file_path: str = Field(nullable=True, index=True)
>>>>>>> main
=======
    file_path: str = Field(nullable=True, index=True)
>>>>>>> main
    total_bill: float = Field(nullable=False)
    sex: str = Field(nullable=False)
    smoker: str = Field(nullable=False)
    day: str = Field(nullable=False)
    time: str = Field(nullable=False)
    size: int = Field(nullable=False)
    tip: float = Field(nullable=False)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> main
=======
>>>>>>> main
    prediction_source: str = Field(nullable=False)
    predicted_at: datetime = Field(nullable=False, index=True)


class DataIssues(ProjectBaseModel, table=True):
    __tablename__ = "data_issues"
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    file_path: str = Field(nullable=False, index=True)
    evaluated_expectations: int = Field(nullable=False)
    successful_expectations: int = Field(nullable=False)
    unsuccessful_expectations: int = Field(nullable=False)
    success_percent: float = Field(nullable=False)
    missing_columns: str = Field(nullable=False)
    missing_values: str = Field(nullable=False)
    duplicated_rows: str = Field(nullable=False)
    unknown_categorical_values: str = Field(nullable=False)
    unknon_numeric_values: str = Field(nullable=False)
    bad_csv_encoding: str = Field(nullable=False)
    bad_csv_format: str = Field(nullable=False)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> main
=======
>>>>>>> main
    created_at: datetime = Field(nullable=False, index=True)


def get_engine():
    session_manager = SessionManager()
    return session_manager.engine


def create_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
