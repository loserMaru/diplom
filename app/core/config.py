from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    docs_url: str
    openapi_url: str
    debug: bool = False

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    secret_key: str
    access_token_expire_minutes: int = 60

    max_image_size_mb: int
    image_allowed_types: str

    supabase_url: str
    supabase_service_role_key: str
    supabase_bucket_museums: str
    supabase_bucket_exhibits: str

    database_url_sync: str

    base_dir: Path = Path(__file__).resolve().parent.parent.parent

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

MAX_IMAGE_SIZE = settings.max_image_size_mb * 1024 * 1024
ALLOWED_IMAGE_TYPES = set(settings.image_allowed_types.split(","))
