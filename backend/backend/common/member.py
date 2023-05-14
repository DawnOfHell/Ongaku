from dataclasses import dataclass


@dataclass
class RoomMember:
    id: str
    name: str
    score: int = 0
    leader: bool = False

    def add_to_score(self, score):
        self.score += score
