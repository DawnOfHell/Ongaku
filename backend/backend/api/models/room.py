from pydantic import BaseModel


class RoomId(BaseModel):
    room_id: str


class UpdateLeader(BaseModel):
    room_id: str
    player_id: str
    new_leader_id: str

