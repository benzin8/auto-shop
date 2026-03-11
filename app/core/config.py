from pydantic_settings import BaseSettings

class Settings (BaseSettings):
    db_url: str
    secret_key: str
    class Config:
        env_file = "config.env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

def load_settings() -> Settings:
    return Settings()
