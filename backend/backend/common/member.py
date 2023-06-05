from dataclasses import dataclass

from .message import UpdateScore

from .websocket_handler import GameWebsocketHandler


@dataclass
class RoomMember:
    id: str
    name: str
    score: int = 0
    leader: bool = False
    websocket: GameWebsocketHandler = None

    def add_to_score(self, score):
        self.score += score
        return UpdateScore(player_id=self.id,
                           new_score=self.score)

    def data(self):
        return {"id": self.id,
                "name": self.name,
                "score": self.score,
                "leader": self.leader}