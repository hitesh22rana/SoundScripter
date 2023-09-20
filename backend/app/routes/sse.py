# Purpose: ServerSideEvents router for handling realtime updates related operations.
# Path: backend\app\routers\sse.py

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from app.services.sse import NotificationsService

router = APIRouter(
    tags=["ServerSideEvents"],
    prefix="/sse",
)


@router.get("/notifications", response_description="Realtime status")
async def notifications():
    return EventSourceResponse(NotificationsService().send_notifications())
