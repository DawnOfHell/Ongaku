from pydantic import BaseModel


class PlayerId(BaseModel):
    player_id: str


class PlayerName(BaseModel):
    player_name: str
