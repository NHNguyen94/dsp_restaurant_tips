from src.services.data_pipelines.predict import run_check_new_data


class TestDataPipelines:
    def test_run_check_new_data(self):
        new_files = run_check_new_data(0)
        print(f"\nnew_files: {new_files}")
