import uuid

from fastapi import HTTPException, status
from cached_property import cached_property

from .player import Player


class Room:
    def __init__(self):
        self._players = {}

    @property
    def players(self):
        return self._players

    @property
    def leader(self):
        leader = next(filter(lambda player: player.leader
                             , self._players.values()))
        return leader

    @cached_property
    def room_id(self):
        return uuid.uuid4().hex[0:6]

    def add_player(self, player: Player):
        self._players.update({player.id: player})

    def update_leader(self, player_id, new_leader_id):
        player = self._players.get(player_id)
        new_leader = self._players.get(new_leader_id)

        if not player or not new_leader:
            raise HTTPException(
                detail="One of the given player ids does not exist in room",
                status_code=status.HTTP_404_NOT_FOUND)

        if not player.leader:
            raise HTTPException(detail=f"Player {player.name} is not room admin",
                                status_code=status.HTTP_401_UNAUTHORIZED)

        player.leader = False
        new_leader.leader = True


