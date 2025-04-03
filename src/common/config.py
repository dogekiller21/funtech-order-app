from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    db_host: str = Field(alias="DB_HOST", default="db")
    db_port: int = Field(alias="DB_PORT", default=5432)
    db_name: str = Field(alias="DB_NAME", default="funtech")
    db_user: str = Field(alias="DB_USER", default="funtech")
    db_password: str = Field(alias="DB_PASSWORD")

    def get_sync_db_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def get_async_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class AppSettings(BaseSettings):
    jwt_auth_secret: str = Field(alias="JWT_AUTH_SECRET")


class RedisSettings(BaseSettings):
    redis_host: str = Field(alias="REDIS_HOST", default="redis")
    redis_port: int = Field(alias="REDIS_PORT", default=6379)
    redis_db: int = Field(alias="REDIS_DB", default=0)
    redis_password: str | None = Field(alias="REDIS_PASSWORD", default=None)
    ttl: int = Field(alias="REDIS_TTL", default=300)

    def get_url(self) -> str:
        password_str = f":{self.redis_password}@" if self.redis_password else ""
        return (
            f"redis://{password_str}{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )


class RabbitMQSettings(BaseSettings):
    host: str = Field(alias="RABBITMQ_HOST", default="rabbitmq")
    port: int = Field(alias="RABBITMQ_PORT", default=5672)
    username: str = Field(alias="RABBITMQ_USERNAME", default="guest")
    password: str = Field(alias="RABBITMQ_PASSWORD", default="guest")
    queue: str = Field(alias="RABBITMQ_QUEUE", default="orders")
    routing_key: str = Field(alias="RABBITMQ_ROUTING_KEY", default="orders.create")

    prefetch_count: int = Field(alias="RABBITMQ_PREFETCH_COUNT", default=10)

    def get_url(self) -> str:
        return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"


@lru_cache()
def get_db_settings() -> DBSettings:
    return DBSettings()


@lru_cache()
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache()
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


@lru_cache()
def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()
