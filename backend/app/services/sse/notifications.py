# Purpose: Notifications service for handling notifications related tasks.
# Path: backend\app\services\sse\notifications.py

import asyncio
from enum import Enum

from fastapi import HTTPException, status

from app.utils.redis_client import redis_client


class Channels(str, Enum):
    status = "status"


class NotificationsService:
    def __init__(self):
        pass

    def publish_message(self, channel: Channels, message: str) -> None:
        """
        Publishes a message to a channel
        :param -> channel: Channels, message: str
        :return -> None
        """

        try:
            redis_client.publish_sync(channel=channel, message=message)

        except Exception as e:
            print(e)

    async def send_notifications(self):
        status_channel = await redis_client.subscribe_async(Channels.status)

        try:
            while True:
                message = await status_channel.get_message()
                if message:
                    yield {"event": "message", "data": message}

                await asyncio.sleep(0)

        except asyncio.exceptions.CancelledError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Notification service is not available"

            raise HTTPException(status_code=status_code, detail=detail) from e
