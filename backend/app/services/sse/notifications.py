# Purpose: Notifications service for handling notifications related tasks.
# Path: backend\app\services\sse\notifications.py

import asyncio

from fastapi import HTTPException, status

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

    async def send(self):
        status_channel = await redis_client.subscribe_async(Channels.STATUS)

        try:
            while True:
                message = await status_channel.get_message()
                if message:
                    yield {"event": "message", "data": message}

                await asyncio.sleep(0)

        except asyncio.exceptions.CancelledError as e:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Error: Notification service is not available"

            if e.args and isinstance(e.args[0], dict):
                status_code = e.args[0].get("status_code")
                detail = e.args[0].get("detail")

            raise HTTPException(status_code=status_code, detail=detail) from e
