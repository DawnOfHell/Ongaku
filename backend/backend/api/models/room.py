from pydantic import BaseModel


class RoomId(BaseModel):
    room_id: str
