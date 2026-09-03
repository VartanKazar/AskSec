from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Define variables with their expected types
    APP_NAME: str = "AskSec"  # Has a default value if not in .env
    DEBUG: bool                        # Automatically converted to True/False
    #DATABASE_URL: PostgresDsn
    DATABASE_URL: str          # Validates that it's a real Postgres URL
    API_TIMEOUT: int = 10             # Automatically parsed into an integer

    # Tell Pydantic to read from a .env file
    model_config = SettingsConfigDict(
        env_file="../.env", 
        env_file_encoding="utf-8",
        extra="ignore"                 # Ignores extra environment variables not typed here
    )

# Instantiate the settings to use throughout the app
settings = Settings()