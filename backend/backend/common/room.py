import uuid
from typing import Any
from datetime import datetime
from pydantic import BaseModel
from .message_dtos import Message, ClientContent
from cached_property import cached_property

from .turn import Turn
from .member import RoomMember

from backend.errors.room import PlayerNotInRoomError, PlayerIsNotLeaderError
from backend.common.websocket_handler import GameWebsocketHandler, WebSocket


class Room:
    def __init__(self):
        self._members: dict[str, RoomMember] = {}
        self.turn: Turn = None

    @property
    def members(self):
        return self._members

    @property
    def leader(self):
        leader = next(filter(lambda player: player.leader
                             , self._members.values()))
        return leader

    @cached_property
    def room_id(self):
        return uuid.uuid4().hex[0:6]

    def add_member(self, member: RoomMember):
        self._members.update({member.id: member})

    def update_leader(self, player_id: str, new_leader_id: str):
        player = self._members.get(player_id)
        new_leader = self._members.get(new_leader_id)

        if not player or not new_leader:
            raise PlayerNotInRoomError(players=[player_id, new_leader_id])

        if not player.leader:
            raise PlayerIsNotLeaderError(player_name=player.name)

        player.leader = False
        new_leader.leader = True

    def get_room_member(self, player_id: str) -> RoomMember:
        member = self._members.get(player_id)
        if not member:
            raise PlayerNotInRoomError(players=[player_id])

        return member

    async def _broadcast(self, message: BaseModel):
        message = Message(timestamp=datetime.now(),
                          content=message)
        for member in self._members.values():
            await member.websocket.send(message)

    async def _on_receive(self, member: RoomMember, payload: Any):
        new_content = None
        if self.turn.current_song and payload.content == self.turn.current_song:
            score = self.turn.calculate_score(payload)
            new_content = member.add_to_score(score)

        message = new_content or ClientContent(sender=member.name,
                                               text=payload)
        await self._broadcast(message)

    async def upgrade_to_ws(self, player_id: str, websocket: WebSocket):
        member = self.get_room_member(player_id)
        member.websocket = GameWebsocketHandler(member,
                                                websocket,
                                                self._on_receive)
        return member
