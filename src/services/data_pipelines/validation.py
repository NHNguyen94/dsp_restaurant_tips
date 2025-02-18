from src.services.data_pipelines.models.bad_data import Anomaly


def _compute_anomaly(self, df: pd.DataFrame) -> Anomaly:
    return Anomaly(
        total_null=df.isnull().sum().sum(),
        total_missing_columns=df.isnull().any(axis=1).sum(),
        total_wrong_dtype=0,
        total_wrong_format=0,
        total_not_accept_value=0,
    )
