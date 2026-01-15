from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_EXPIRE: int = 3600

    class Config:
        env_file = '../.env'


settings = Settings()
