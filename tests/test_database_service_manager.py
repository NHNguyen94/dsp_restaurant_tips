from src.database.service_manager import DatabaseServiceManager


class TestDataBaseServiceManager:
    service_manager = DatabaseServiceManager()

    def test_get_recent_predicted_files(self):
        recent_predicted_files = self.service_manager.get_predicted_files(0)
        print(f"\nrecent_predicted_files: {recent_predicted_files}")
