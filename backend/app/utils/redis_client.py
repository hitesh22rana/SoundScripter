# Purpose: Redis client for handling pub-sub tasks
# Path: backend\app\utils\redis_client.py

import sys

from loguru import logger
from redis import Redis as SyncRedis
from redis.asyncio import Redis as AsyncRedis

from app.config import settings


class RedisClient:
    sync_client: SyncRedis = None
    async_client: AsyncRedis = None

    sync_pubsub = None
    async_pubsub = None

    redis_host: str = settings.redis_host
    redis_port: int = settings.redis_port

    logger.configure(
        handlers=[
            dict(sink=sys.stdout, level="INFO", colorize=True),
            dict(sink=sys.stderr, level="CRITICAL", colorize=True),
        ],
    )

    @classmethod
    def __init__(cls) -> None | Exception:
        cls.connect()

    @classmethod
    def connect(cls) -> None | Exception:
        try:
            if not cls.sync_client or not cls.async_client:
                cls.sync_client = SyncRedis(host=cls.redis_host, port=cls.redis_port)

                cls.async_client = AsyncRedis(
                    host=cls.redis_host,
                    port=cls.redis_port,
                    auto_close_connection_pool=False,
                )

                cls.sync_pubsub = cls.sync_client.pubsub()
                cls.async_pubsub = cls.async_client.pubsub()

                logger.info("Success: Redis client connected")

        except Exception as _:
            logger.critical("Error: Redis client could not be connected")
            raise Exception()

    @classmethod
    def disconnect(cls) -> None | Exception:
        try:
            if cls.sync_client and cls.async_client:
                cls.sync_client.close()
                cls.async_client.close()
                logger.info("Success: Redis client disconnected")

        except Exception as _:
            logger.critical("Error: Redis client could not be disconnected")
            raise Exception()

    @classmethod
    def get_sync_client(cls) -> SyncRedis | None:
        return cls.sync_client

    @classmethod
    def get_async_client(cls) -> AsyncRedis | None:
        return cls.async_client

    @classmethod
    def publish_sync(cls, channel: str, message: str) -> None:
        cls.sync_client.publish(channel, message)

    @classmethod
    async def publish_async(cls, channel: str, message: str) -> None:
        await cls.async_client.publish(channel, message)

    @classmethod
    def subscribe_sync(cls, channel: str) -> SyncRedis | None:
        cls.sync_pubsub.subscribe(channel)
        return cls.sync_pubsub

    @classmethod
    async def subscribe_async(cls, channel: str) -> AsyncRedis | None:
        await cls.async_pubsub.subscribe(channel)
        return cls.async_pubsub

    @classmethod
    def unsubscribe_sync(cls, channel: str = None) -> SyncRedis | None:
        cls.sync_pubsub.unsubscribe(channel)
        return cls.sync_pubsub

    @classmethod
    async def unsubscribe_async(cls, channel: str = None) -> AsyncRedis | None:
        await cls.async_pubsub.unsubscribe(channel)
        return cls.async_pubsub


redis_client = RedisClient()
