from typing import final

from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    api_token: str
    webhook_path: str
    webhook_url: str
    my_token: str
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    DB_NAME: str = 'DiaryDB'
    DB_COLLECTION: str = 'diary'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
