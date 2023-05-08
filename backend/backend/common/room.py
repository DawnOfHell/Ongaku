import uuid

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
