import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()


class SessionManager:
    # https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/#use-the-dependency
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))
        self.Session = sessionmaker(bind=self.engine)

    def close(self):
        self.engine.dispose()

    def connect(self):
        return self.engine.connect()

    def session(self):
        return self.Session()
