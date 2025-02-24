from typing import List

from sqlmodel import select, col, and_

from src.database.models import PredictedFiles, Predictions
from src.database.session_manager import SessionManager
from src.utils import DateTimeManager


class DatabaseServiceManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.session = self.session_manager.session()
        self.async_session = self.session_manager.async_session()

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

    def append_files_to_predicted_files_table(self, file_names: List[str]) -> None:
        with self.session as session:
            for file_name in file_names:
                predicted_file = PredictedFiles(
                    file_name=file_name,
                    created_at=DateTimeManager.get_current_local_time(),
                )
                session.add(predicted_file)
            session.commit()

    def get_predicted_files(self, hours_ago: int) -> List[PredictedFiles]:
        # https://sqlmodel.tiangolo.com/tutorial/where/#type-annotations-and-errors
        with self.session as session:
            query = select(PredictedFiles)
            # https://sqlmodel.tiangolo.com/tutorial/select/#sqlmodels-sessionexec
            return session.execute(query).scalars().all()

    def add_completed_at_to_unpredicted_files(
        self, unpredicted_files: List[PredictedFiles]
    ) -> None:
        with self.session as session:
            for unpredicted_file in unpredicted_files:
                unpredicted_file.completed_at = DateTimeManager.get_current_local_time()
                session.add(unpredicted_file)
            session.commit()
