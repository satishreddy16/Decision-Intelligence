import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    db_path: str = os.getenv("DB_PATH", "data/app.db")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    decision_log_csv: str = os.getenv("DECISION_LOG_CSV", "outputs/decision_log.csv")

SETTINGS = Settings()
