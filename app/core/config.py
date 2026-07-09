from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "changeme-before-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    app_name: str = "SteezyFX API"
    debug: bool = False

    model_config = {"env_file": ".env"}


settings = Settings()