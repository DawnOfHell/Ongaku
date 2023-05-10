from pydantic import BaseModel

from backend.api.models.player import PlayerId

class RoomId(BaseModel):
    room_id: str

class UpdateLeader(BaseModel):
    room_id: RoomId
    player_id: PlayerId
    new_leader_id: PlayerId

