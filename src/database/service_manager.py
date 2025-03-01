from typing import List

<<<<<<< HEAD
from sqlmodel import select, col, func

from src.database.models import Predictions
from src.database.session_manager import SessionManager
=======
import pandas as pd
from sqlmodel import select, col, func

from src.database.models import Predictions, DataIssues
from src.database.session_manager import SessionManager
from src.utils.date_time_manager import DateTimeManager
>>>>>>> main


class DatabaseServiceManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.session = self.session_manager.session()
        self.async_session = self.session_manager.async_session()

<<<<<<< HEAD
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

=======
    def append_data_issues(self, data_issues: DataIssues) -> None:
        with self.session as session:
            session.add(data_issues)
            session.commit()

    def append_df_to_predictions(self, df_with_predictions: pd.DataFrame, prediction_source) -> None:
        with self.session as session:
            # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html
            for _, row in df_with_predictions.iterrows():
                prediction = Predictions(
                    file_path=None,
                    total_bill=row["total_bill"],
                    sex=row["sex"],
                    smoker=row["smoker"],
                    day=row["day"],
                    time=row["time"],
                    size=row["size"],
                    tip=row["tip"],
                    prediction_source=prediction_source,
                    predicted_at=DateTimeManager.get_current_local_time(),
                )
                session.add(prediction)
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

>>>>>>> main
    def get_predicted_files(self, new_files: List[str]) -> List[str]:
        # https://sqlmodel.tiangolo.com/tutorial/where/#type-annotations-and-errors
        with self.session as session:
            # https://sqlmodel.tiangolo.com/tutorial/select/#sqlmodels-sessionexec
            query = select(Predictions.file_path).where(
<<<<<<< HEAD
                col(Predictions.file_path).in_(new_files)
=======
                col(Predictions.file_path).in_(new_files),
                col(Predictions.file_path).is_not(None),
>>>>>>> main
            )
            predicted_files = session.execute(query).all()
            predicted_files = [
                predicted_file.file_path for predicted_file in predicted_files
            ]
            return predicted_files

<<<<<<< HEAD
    def get_predicted_results_by_date(self, date: str) -> List[Predictions]:
        with self.session as session:
            query = select(Predictions).where(func.date(Predictions.created_at) == date)
=======
    def get_predicted_results_by_date_range(
        self, start_date: str, end_date: str, prediction_source: str
    ) -> List[Predictions]:
        if prediction_source == "all":
            prediction_source = ["webapp", "scheduled_predictions"]
        else:
            prediction_source = [prediction_source]
        with self.session as session:
            query = select(Predictions).where(
                func.date(Predictions.predicted_at).between(start_date, end_date),
                col(Predictions.prediction_source).in_(prediction_source),
            )
>>>>>>> main
            predictions = session.execute(query).all()
            return predictions
