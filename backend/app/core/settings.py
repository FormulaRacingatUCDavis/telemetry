from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CAN_INTAKE_PATH: str
    CAN_STAGING_PATH: str
    CAN_RAW_PATH: str
    CAN_PROCESSED_PATH: str
    CAN_REPORTS_PATH: str

    DBC_DIR: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()