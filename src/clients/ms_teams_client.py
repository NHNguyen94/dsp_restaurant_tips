import os

import dotenv
import pymsteams

dotenv.load_dotenv()


class MSTeamsClient:
    def __init__(self):
        self.webhook_url = os.getenv("MS_TEAMS_WEBHOOK_URL")
        self.teams_client = pymsteams.connectorcard(self.webhook_url)

    def send_message(self, message: str) -> bool:
        self.teams_client.text(message)
        return self.teams_client.send()
