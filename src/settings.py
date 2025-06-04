from collections.abc import AsyncGenerator, AsyncIterable

import aiokafka
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # app settings
    APP_NAME: str = Field(default="warehouses")
    APP_DESCRIPTION: str = Field(default="warehouses")
    SWAGGER_PATH: str = Field(default="/docs")

    TESTING: bool = Field(default=False)

    # db
    PG_HOST: str = Field(default="0.0.0.0")
    PG_PORT: int = Field(default=5432)
    PG_DB: str = Field(default="db")
    PG_USER: str = Field(default="user")
    PG_PASSWORD: str = Field(default="strong_password")

    @property
    def pg_db(self) -> str:
        return f"test_{self.PG_DB}" if self.TESTING else self.PG_DB

    @property
    def pg_url(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.pg_db}"

    @property
    def pg_url_sync(self) -> str:
        return f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.pg_db}"

    async def get_repository(self) -> AsyncGenerator[AsyncEngine]:
        yield create_async_engine(url=self.pg_url)

    # kafka consumer
    KAFKA_READING_TOPICS: list[str] = Field(default_factory=list)
    KAFKA_BOOTSTRAP: str = Field(default="127.0.0.1:29092")
    KAFKA_CONSUMER_NAME: str = Field(default="movements-collector")
    KAFKA_OFFSET: str = Field(default="latest")
    KAFKA_RETRY_BACKOFF: int = Field(default=1)
    KAFKA_AUTO_COMMIT: bool = Field(default=False)

    KAFKA_TIMEOUT_MS: int = Field(default=6000)
    KAFKA_BATCH_SIZE: int = Field(default=1000)

    async def get_kafka_consumer(self) -> AsyncIterable[aiokafka.AIOKafkaConsumer]:
        consumer = aiokafka.AIOKafkaConsumer(
            *self.KAFKA_READING_TOPICS,
            bootstrap_servers=self.KAFKA_BOOTSTRAP,
            group_id=self.KAFKA_CONSUMER_NAME,
            auto_offset_reset=self.KAFKA_OFFSET,
            enable_auto_commit=self.KAFKA_AUTO_COMMIT,
            retry_backoff_ms=self.KAFKA_RETRY_BACKOFF * 1000,
        )
        await consumer.start()

        yield consumer

        await consumer.stop()

    # logger
    LOG_LEVEL: int = Field(default=5)

    # Daemons
    DAEMON_RESTART_SEC: int = Field(default=4)


settings = Settings()
