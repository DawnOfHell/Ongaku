from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket

from backend.common.room import Room

from backend.api.models.player import Player

from backend.api.dependencies.room import get_room_by_id
from backend.api.dependencies.player import get_player_by_id

router = APIRouter(tags=["game"])


@router.websocket("/ready/{room_id}/{player_id}")
async def ready(room: Annotated[Room, Depends(get_room_by_id)],
    player: Annotated[Player, Depends(get_player_by_id)],
    websocket: WebSocket):
    await websocket.accept()
    member = await room.upgrade_to_ws(player.player_id, websocket)
    await member.websocket.receive_messages_event()



