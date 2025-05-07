from src.services.data_pipelines.predict import (
    run_check_new_data,
    get_predicted_files,
    run_predict_single_file,
    run_predictions,
)


class TestDataPipelines:
    def test_get_predicted_files(self):
        file_names = ["tests/resources/test_tips.csv"]
        predicted_files = get_predicted_files(file_names)
        print(f"\npredicted_files: {predicted_files}")

    def test_run_check_new_data(self):
        try:
            new_files = run_check_new_data()
            # It can fail if the AirflowException is raised, it's okay
            print(f"\nnew_files: {new_files}")
        except Exception as e:
            print(f"\nNo files to check: {e}")

    # Enable when needed only, this will write into DB
    # def test_run_predict_single_file(self):
    #     file_path = "tests/resources/test_tips.csv"
    #     response = run_predict_single_file(file_path, prediction_source="test")
    #     print(f"\nresponse from single file prediction: {response}")

    # Enable when needed only, this will write into DB
    # def test_run_predictions(self):
    #     file_paths = [
    #         "tests/resources/test_tips.csv",
    #     ]
    #     run_predictions(file_paths)
    #     print("\nPredictions saved to database.")
