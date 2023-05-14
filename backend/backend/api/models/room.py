from pydantic import BaseModel


class RoomId(BaseModel):
    room_id: str


class UpdateLeader(BaseModel):
    player_id: str
    other_id: str
