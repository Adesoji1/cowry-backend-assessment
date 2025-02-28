import os
from dotenv import load_dotenv


env_file = os.path.join(os.path.dirname(__file__), '../.env.admin')
load_dotenv(env_file)

class Settings:
    ADMIN_DB_URL: str = os.getenv("ADMIN_DB_URL", "")
    FRONTEND_SERVICE_URL: str = os.getenv("FRONTEND_SERVICE_URL", "")

settings = Settings()
