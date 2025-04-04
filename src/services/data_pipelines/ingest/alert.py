from src.clients.ms_teams_client import MSTeamsClient
from src.services.data_pipelines.models import ValidatedResult

ms_teams_client = MSTeamsClient()


def run_alert(validated_result: ValidatedResult) -> None:
    if (
        validated_result.csv_results.good_encoding
        and validated_result.csv_results.good_delimiter
        and validated_result.csv_results.no_other_parse_issues
    ):
        ms_teams_client.send_message(
            f"Bad data detected in file: {validated_result.file_path}, details in the report: {validated_result.docs_urls}"
        )
    else:
        ms_teams_client.send_message(
            f"Error in parsing csv file: {validated_result.file_path}"
        )
