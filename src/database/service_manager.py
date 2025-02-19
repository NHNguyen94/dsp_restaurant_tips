from src.database.models import FileRegistration, DataIssues
from src.database.session_manager import SessionManager
from typing import List
from sqlmodel import select, col


class DatabaseServiceManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.session = self.session_manager.session

    def append_file_registration(self, file_path: str) -> None:
        with self.session() as session:
            session.add(FileRegistration(file_path=file_path))
            session.commit()

    def append_data_issue(
        self,
        file_path: str,
        row_missing: int,
        rows_unknown_value: int,
        rows_invalid_value: int,
        rows_outlier: int,
        features_missing: int,
        label_missing: int,
    ) -> None:
        with self.session() as session:
            file_registration = (
                session.query(FileRegistration)
                .filter(FileRegistration.file_path == file_path)
                .first()
            )
            session.add(
                DataIssues(
                    file_id=file_registration.file_id,
                    row_missing=row_missing,
                    rows_unknown_value=rows_unknown_value,
                    rows_invalid_value=rows_invalid_value,
                    rows_outlier=rows_outlier,
                    features_missing=features_missing,
                    label_missing=label_missing,
                )
            )
            session.commit()

    def get_file_registrations(self, file_ids: List[str]) -> List[FileRegistration]:
        # https://sqlmodel.tiangolo.com/tutorial/where/#type-annotations-and-errors
        with self.session() as session:
            query = select(FileRegistration).where(
                col(FileRegistration.file_id).in_(file_ids)
            )
            return session.exec(query).all()
