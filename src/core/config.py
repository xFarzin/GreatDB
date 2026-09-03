from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_name: str = "SearchPlatform"
    debug: bool = False
    environment: str = "production"

    # DB
    database_url: str

    # OpenSearch
    opensearch_url: str
    opensearch_user: str = "admin"
    opensearch_password: str

    # Redis
    redis_url: str
    celery_broker_url: str

    # MinIO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool = False

    # Telegram
    telegram_bot_token: str
    admin_ids: str = "" # Comma separated

    @property
    def admin_ids_list(self) -> List[int]:
        if not self.admin_ids:
            return []
        return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
