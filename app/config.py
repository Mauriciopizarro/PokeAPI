from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_EXPIRE: int = 3600

    model_config = ConfigDict(env_file='../.env')


settings = Settings()
