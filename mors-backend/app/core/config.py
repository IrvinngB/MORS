from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MORS API"
    debug: bool = True
    narrative_mode: str = "local"
    anthropic_api_key: str = ""
    session_ttl_hours: int = 6

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()