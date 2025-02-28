from typing import List

from sqlmodel import select, col, func

from src.database.models import Predictions, DataIssues
from src.database.session_manager import SessionManager


class DatabaseServiceManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.session = self.session_manager.session()
        self.async_session = self.session_manager.async_session()

    def append_data_issues(self, data_issues: DataIssues) -> None:
        with self.session as session:
            session.add(data_issues)
            session.commit()

    def append_predictions(self, predictions: List[Predictions]) -> None:
        with self.session as session:
            for prediction in predictions:
                session.add(prediction)
            session.commit()

    async def async_append_predictions(self, predictions: List[Predictions]) -> None:
        async with self.async_session as session:
            for prediction in predictions:
                session.add(prediction)
            await session.commit()

    def get_predicted_files(self, new_files: List[str]) -> List[str]:
        # https://sqlmodel.tiangolo.com/tutorial/where/#type-annotations-and-errors
        with self.session as session:
            # https://sqlmodel.tiangolo.com/tutorial/select/#sqlmodels-sessionexec
            query = select(Predictions.file_path).where(
                col(Predictions.file_path).in_(new_files),
                col(Predictions.file_path).is_not(None),
            )
            predicted_files = session.execute(query).all()
            predicted_files = [
                predicted_file.file_path for predicted_file in predicted_files
            ]
            return predicted_files

    def get_predicted_results_by_date_range(
        self, start_date: str, end_date: str
    ) -> List[Predictions]:
        with self.session as session:
            query = select(Predictions).where(
                func.date(Predictions.predicted_at).between(start_date, end_date)
            )
            predictions = session.execute(query).all()
            return predictions
