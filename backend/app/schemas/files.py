# Purpose: Files schema
# Path: backend\app\schemas\files.py

from app.models import FilesModel
from app.utils.shared import Status, Type


class FileResponse:
    def __init__(self, data: FilesModel) -> None:
        self.id: str = data.id
        self.type: Type = data.type
        self.path: str = data.path
        self.status: Status = data.status
        self.created_at: str = data.created_at.isoformat()
        self.completed_at: str = (
            data.completed_at.isoformat() if data.completed_at else None
        )

    def response(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }
