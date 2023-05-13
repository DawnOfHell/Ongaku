from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from backend.common.room import Room
from backend.common.player import Player
from backend.api.models.room import RoomId, UpdateLeader
from backend.api.models.player import PlayerId
from backend.api.routes.player import get_players

router = APIRouter(tags=["rooms"])


@lru_cache
def get_rooms() -> dict[str, Room]:
    return {}


@router.post("/rooms/", status_code=status.HTTP_201_CREATED,
             response_model=RoomId)
async def create_room(player_id: PlayerId,
                      rooms: Annotated[dict[str, Room], Depends(get_rooms)],
                      players: Annotated[dict[str, str], Depends(get_players)]):
    room = Room()
    player_name = players.get(player_id.player_id)

    if not player_name:
        raise HTTPException(detail=f"no user under given id {player_id.player_id}",
                             status_code=status.HTTP_404_NOT_FOUND)

    player = Player(id=player_id.player_id,
                    name=player_name)
    player.leader = True
    room.add_player(player)
    rooms.update({room.room_id: room})
    return RoomId(room_id=room.room_id)


@router.post("/enter_room/room_id",
             status_code=status.HTTP_202_ACCEPTED)
async def enter_room(room_id: RoomId,
                     player_id: PlayerId,
                     rooms: Annotated[dict[str, Room], Depends(get_rooms)],
                     players: Annotated[dict[str, str], Depends(get_players)]):
    room = rooms.get(room_id.room_id)
    if not room:
        return HTTPException(detail=f"no such room {room_id.room_id}",
                             status_code=status.HTTP_404_NOT_FOUND)

    player_in_room = room.players.get(player_id.player_id)
    if player_in_room:
        return

    player_name = players.get(player_id.player_id)

    if not player_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"no user under given id {player_id.player_id}")

    player = Player(id=player_id.player_id,
                    name=player_name)

    room.add_player(player)


@router.post("/get_room_players/",
            status_code=status.HTTP_200_OK,
            response_model=list[Player])
async def get_room_players(room_id: RoomId,
                      rooms: Annotated[dict[str, Room], Depends(get_rooms)]):
    room = rooms.get(room_id.room_id)
    if not room:
        raise HTTPException(detail=f"no such room {room_id.room_id}",
                             status_code=status.HTTP_404_NOT_FOUND)

    return list(room.players.values())


@router.put("/change_room_leader/",
            status_code=status.HTTP_204_NO_CONTENT)
async def update_room_leader(update_leader: UpdateLeader,
                             rooms: Annotated[dict[str, Room], Depends(get_rooms)]):
    room = rooms.get(update_leader.room_id)
    if not room:
        raise HTTPException(detail="Room does not exist!",
                             status_code=status.HTTP_404_NOT_FOUND)

    room.update_leader(player_id=update_leader.player_id,
                       new_leader_id=update_leader.new_leader_id)


@router.delete("/delete_room/",
               status_code=status.HTTP_200_OK)
async def delete_room(room_id: RoomId,
                      rooms: Annotated[dict[str, Room], Depends(get_rooms)]):
    room = rooms.get(room_id.room_id)
    if room:
        return rooms.pop(room.room_id)
