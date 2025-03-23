from datetime import datetime, timezone, timedelta, date


class DateTimeManager:
    @staticmethod
    def get_current_utc_time_str() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_local_time_str() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_local_time() -> datetime:
        return datetime.now()

    @staticmethod
    def get_hours_ago_str(hours_ago: int) -> str:
        return (datetime.now() - timedelta(hours=hours_ago)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    @staticmethod
    def parse_str_to_date(date_str: str) -> date:
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    @staticmethod
    def parse_datetime_to_str(date_time: datetime) -> str:
        return date_time.strftime("%Y-%m-%d %H:%M:%S")
