<<<<<<< HEAD
from src.services.data_pipelines.models.validated_result import ValidatedResult
=======
from src.services.data_pipelines.models import ValidatedResult
>>>>>>> main
from src.clients.ms_teams_client import MSTeamsClient

ms_teams_client = MSTeamsClient()


def run_alert(validated_result: ValidatedResult) -> None:
    bad_df = validated_result.final_df[validated_result.final_df["is_good"] == 0]
    if bad_df.shape[0] > 0:
        ms_teams_client.send_message(
            f"Bad data detected in file: {validated_result.file_path}, details in the report: {validated_result.docs_urls}"
        )
