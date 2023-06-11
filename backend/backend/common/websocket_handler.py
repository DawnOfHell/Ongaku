from pydantic import BaseModel
from typing import TypeVar, Callable

from .message import Message

WebSocket = TypeVar("WebSocket")
RoomMember = TypeVar("RoomMember")


class GameWebsocketHandler(BaseModel):
    _member: RoomMember
    _websocket: WebSocket
    _receive_callback: Callable

    async def receive_messages_event(self):
        async for message in self._websocket.iter_text():
            await self._receive_callback(self._member, message)

    async def send(self, message: Message):
        await self._websocket.send_json(message.json())