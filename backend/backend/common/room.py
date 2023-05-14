import uuid

from cached_property import cached_property

from .member import RoomMember

from backend.api.errors.room import PlayerNotInRoom, PlayerIsNotLeader


class Room:
    def __init__(self):
        self._members = {}

    @property
    def members(self):
        return self._members

    @property
    def leader(self):
        leader = next(filter(lambda player: player.leader
                             , self._players.values()))
        return leader

    @cached_property
    def room_id(self):
        return uuid.uuid4().hex[0:6]

    def add_member(self, member: RoomMember):
        self._members.update({member.id: member})

    def update_leader(self, player_id, new_leader_id):
        player = self._members.get(player_id)
        new_leader = self._members.get(new_leader_id)

        if not player or not new_leader:
            raise PlayerNotInRoom(players=[player_id, new_leader_id])

        if not player.leader:
            raise PlayerIsNotLeader(player_name=player.name)

        player.leader = False
        new_leader.leader = True


