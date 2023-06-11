from typing import Annotated, Union

from fastapi import APIRouter, Depends, status

from backend.common.room import Room
from backend.common.member import RoomMember

from backend.api.models.room import RoomId
from backend.api.models.player import Player

from backend.api.dependencies.room import rooms, get_room_by_id
from backend.api.dependencies.player import (get_player_by_id,
                                             get_other_by_id,
                                             get_player_by_id_body)

router = APIRouter(tags=["rooms"])


@router.post("/rooms", status_code=status.HTTP_201_CREATED,
             response_model=RoomId)
async def create_room(player: Annotated[Player, Depends(get_player_by_id_body)],
                      rooms: Annotated[dict[str, Room], Depends(rooms)]):
    room = Room()

    player = RoomMember(id=player.player_id,
                        name=player.player_name)
    player.leader = True
    room.add_member(player)
    rooms.update({room.room_id: room})
    return RoomId(room_id=room.room_id)


@router.post("/rooms/{room_id}/{player_id}",
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


@router.get("/rooms/{room_id}/players",
            status_code=status.HTTP_200_OK,
            response_model=list[dict[str, Union[str, int]]])
async def get_room_players(room: Annotated[Room, Depends(get_room_by_id)]):
    return [value.data for value in room.members.values()]


@router.put("/room_leader/{room_id}/leader",
            status_code=status.HTTP_204_NO_CONTENT)
async def update_room_leader(room: Annotated[Room, Depends(get_room_by_id)],
                             player: Annotated[Player, Depends(get_player_by_id_body)],
                             other: Annotated[Player, Depends(get_other_by_id)]):
    room.update_leader(player_id=player.player_id,
                       new_leader_id=other.player_id)


@router.delete("/rooms/{room_id}",
               status_code=status.HTTP_200_OK)
def delete_room(room: Annotated[Room, Depends(get_room_by_id)],
                rooms: Annotated[dict[str, Room], Depends(rooms)]):
    return rooms.pop(room.room_id)
