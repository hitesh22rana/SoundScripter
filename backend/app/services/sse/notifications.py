# Purpose: Notifications service for handling notifications related tasks.
# Path: backend\app\services\sse\notifications.py

import asyncio
from typing import AsyncGenerator

from app.utils.redis_client import redis_client
from app.utils.shared import Channels


class NotificationsService:
    def __init__(self):
        pass

    def publish(self, channel: str, message: str) -> None:
        """
        Publishes a message to a channel
        :param -> channel: str, message: str
        :return -> None
        """

        try:
            redis_client.publish_sync(channel=channel, message=message)

        except Exception as e:
            print(e)

    async def send(self) -> AsyncGenerator[str, str]:
        """
        Send message to a subscribed channel.
        :return -> AsyncGenerator[str, str]:
        """

        notifications_channel = await redis_client.subscribe_async(
            Channels.NOTIFICATIONS
        )

        try:
            while True:
                message: dict | None = await notifications_channel.get_message()
                if message and isinstance(message["data"], bytes):
                    yield (message["data"]).decode("utf-8")

                await asyncio.sleep(0)

        except asyncio.exceptions.CancelledError as e:
            raise e

        except Exception as e:
            print(f"Error: {e}")
