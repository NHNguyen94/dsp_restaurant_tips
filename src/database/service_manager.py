from src.database.session_manager import SessionManager


class DatabaseServiceManager:
    def __init__(self):
        self.session_manager = SessionManager()
        self.session = self.session_manager.session
