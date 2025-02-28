import os
from dotenv import load_dotenv

env_file = os.path.join(os.path.dirname(__file__), '../.env.frontend')
load_dotenv(env_file)

class Settings:
    FRONTEND_DB_URL: str = os.getenv("FRONTEND_DB_URL", "")

settings = Settings()
