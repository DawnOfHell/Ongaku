from pydantic import BaseModel

from .message_dtos import UpdateScoreContent

from .websocket_handler import GameWebsocketHandler


class RoomMember(BaseModel):
    id: str
    name: str
    score: int = 0
    leader: bool = False
    websocket: GameWebsocketHandler = None

    def add_to_score(self, score):
        self.score += score
        return UpdateScoreContent(player_id=self.id,
                                  new_score=self.score)
