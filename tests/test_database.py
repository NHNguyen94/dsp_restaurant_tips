from src.database.service_manager import DatabaseServiceManager


class TestDatabase:
    db_service_manager = DatabaseServiceManager()

    def test_get_predicted_results_by_date(self):
        start_date = "2025-02-24"
        end_date = "2025-02-25"
        predicted_results = self.db_service_manager.get_predicted_results_by_date_range(
            start_date, end_date
        )
        print(f"\npredicted_results_by_date: {predicted_results[:3]}")
