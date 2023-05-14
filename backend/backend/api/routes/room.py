from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from backend.common.room import Room
from backend.common.member import RoomMember

from backend.api.models.room import RoomId
from backend.api.models.player import Player

from backend.api.routes.player import get_other_by_id, get_player_by_id

router = APIRouter(tags=["rooms"])


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


@router.post("/rooms/{player_id}", status_code=status.HTTP_201_CREATED,
             response_model=RoomId)
async def create_room(player: Annotated[Player, Depends(get_player_by_id)],
                      rooms: Annotated[dict[str, Room], Depends(rooms)]):
    room = Room()

    player = RoomMember(id=player.player_id,
                        name=player.player_name)
    player.leader = True
    room.add_member(player)
    rooms.update({room.room_id: room})
    return RoomId(room_id=room.room_id)


@router.post("/enter_room/{room_id}/{player_id}",
             status_code=status.HTTP_202_ACCEPTED)
async def enter_room(room: Annotated[Room, Depends(get_room_by_id)],
                     player: Annotated[Player, Depends(get_player_by_id)]):
    player_in_room = room.members.get(player.player_id)
    if player_in_room:
        return {}

    player = RoomMember(id=player.player_id,
                        name=player.player_name)

    room.add_member(player)

    return RoomMember


@router.post("/room_players/{room_id}",
            status_code=status.HTTP_200_OK,
            response_model=list[RoomMember])
async def get_room_players(room: Annotated[Room, Depends(get_room_by_id)]):
    return list(room.members.values())


@router.put("/room_leader/{room_id}/{player_id}/{other_id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def update_room_leader(room: Annotated[Room, Depends(get_room_by_id)],
                             player: Annotated[Player, Depends(get_player_by_id)],
                             other: Annotated[Player, Depends(get_other_by_id)]):
    room.update_leader(player_id=player.player_id,
                       new_leader_id=other.player_id)


@router.delete("/rooms/{room_id}",
               status_code=status.HTTP_200_OK)
async def delete_room(room: Annotated[Room,Depends(get_room_by_id)],
                      rooms: Annotated[dict[str, Room], Depends(rooms)]):
        return rooms.pop(room.room_id)
