import datetime
from typing import TypeVar, Callable

from .message import Message

WebSocket = TypeVar("WebSocket")
RoomMember = TypeVar("RoomMember")


class GameWebsocketHandler:
    def __init__(self, member: RoomMember, websocket: WebSocket, callback: Callable):
        self._member = member
        self._websocket = websocket
        self._receive_callback = callback

    async def receive_messages_event(self):
        async for message in self._websocket.iter_text():
            await self._receive_callback(self._member, message)

    async def send(self, message: Message):
        await self._websocket.send_json(message.json)