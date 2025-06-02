from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # app settings
    APP_NAME: str = Field(default="warehouses")
    APP_DESCRIPTION: str = Field(default="warehouses")
    SWAGGER_PATH: str = Field(default="/docs")


settings = Settings()
