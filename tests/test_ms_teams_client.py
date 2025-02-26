from src.clients.ms_teams_client import MSTeamsClient
from src.utils.date_time_manager import DateTimeManager
from src.utils.helper import get_current_user


class TestMSTeamsClient:
    def test_send_message(self):
        client = MSTeamsClient()
        user = get_current_user()
        message = f"Test message sent at {DateTimeManager.get_current_local_time_str()} from {user}"
        assert client.send_message(message) is True
