from src.services.data_pipelines.models import ValidatedResult
from src.database.service_manager import DatabaseServiceManager

db_service_manager = DatabaseServiceManager()


def run_save_statistics(validated_result: ValidatedResult) -> None:
    pass
