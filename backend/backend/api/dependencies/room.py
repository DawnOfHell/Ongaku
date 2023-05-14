from typing import Annotated
from functools import lru_cache

from fastapi import status, Depends, HTTPException

from backend.common.room import Room


@lru_cache
def rooms() -> dict[str, Room]:
    return {}


def get_room_by_id(room_id: str,
                rooms: Annotated[dict[str, str], Depends(rooms)]):
    room = rooms.get(room_id)
    if not room:
        raise HTTPException(detail=f"room id {room_id} does not exist!",
                            status_code=status.HTTP_404_NOT_FOUND)

    return room
