from pydantic import BaseModel


class Player(BaseModel):
    player_name: str
    player_id: str