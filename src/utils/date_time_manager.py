from datetime import datetime, timezone


class DateTimeManager:
    @staticmethod
    def get_current_utc_time() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_local_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
