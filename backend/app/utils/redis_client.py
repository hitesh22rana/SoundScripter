# # Purpose: Redis client for handling redis operations
# # Path: backend\app\utils\redis_client.py

# import sys

# import redis
# from loguru import logger
# from redis import Redis

# from app.config import settings


# class RedisClient:
#     client: Redis = None
#     host: str = settings.redis_host
#     port: int = settings.redis_port
#     password: str = settings.redis_password

#     logger.configure(
#         handlers=[
#             dict(sink=sys.stdout, level="INFO", colorize=True),
#             dict(sink=sys.stderr, level="CRITICAL", colorize=True),
#         ],
#     )

#     @classmethod
#     def __init__(cls) -> None:
#         cls.connect()

#     @classmethod
#     def connect(cls) -> None:
#         try:
#             if not cls.client:
#                 cls.client = Redis(host=cls.host, port=cls.port, password=cls.password)
#                 logger.info("Success: Redis client initialized")

#         except redis.exceptions.ConnectionError:
#             logger.critical("Error: Redis client could not be initialized")

#     @classmethod
#     def disconnect(cls) -> None:
#         try:
#             if cls.client:
#                 cls.client.close()
#                 logger.info("Success: Redis client disconnected")

#         except redis.exceptions.ConnectionError:
#             logger.critical("Error: Redis client could not be disconnected")

#     @classmethod
#     def get_client(cls) -> Redis | None:
#         if not cls.client:
#             cls.__init__()

#         return cls.client

#     @classmethod
#     def ping(cls) -> bool:
#         if cls.client:
#             return cls.client.ping()

#         return False


# redis_client = RedisClient()
