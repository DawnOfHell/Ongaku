from functools import lru_cache
from typing import Annotated, Union

from fastapi import APIRouter, Depends, status, Response


from backend.common.room import Room
from backend.common.player import Player
from backend.api.models.room import RoomId, UpdateLeader
from backend.api.models.player import PlayerId
from backend.api.routes.player import get_players

router = APIRouter()

@lru_cache
def get_rooms() -> dict:
    return {}


@router.post("/create_room/", tags=["room"], status_code=status.HTTP_201_CREATED,
             response_model=RoomId)
async def create_room(player_id: PlayerId,
                      rooms: Annotated[dict[str, Room], Depends(get_rooms)],
                      players: Annotated[dict[str, str], Depends(get_players)],
                      response: Response):
    room = Room()
    player_name = players.get(player_id.player_id)

    if not player_name:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"no user under given id {player_id.player_id}"

    player = Player(id=player_id.player_id,
                    name=player_name)
    player.leader = True
    room.add_player(player)
    rooms.update({room.room_id: room})
    return RoomId(room_id=room.room_id)


@router.post("/enter_room/",
             tags=["room"],
             status_code=status.HTTP_202_ACCEPTED)
async def enter_room(room_id: RoomId,
                     player_id: PlayerId,
                     rooms: Annotated[dict[str, Room], Depends(get_rooms)],
                     players: Annotated[dict[str, str], Depends(get_players)],
                     response: Response,
                     ):
    room = rooms.get(room_id.room_id)
    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"no such room {room_id.room_id}"

    player_in_room = room.players.get(player_id.player_id)
    if player_in_room:
        return

    player_name = players.get(player_id.player_id)

    if not player_name:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"no user under given id {player_id.player_id}"

    player = Player(id=player_id.player_id,
                    name=player_name)

    room.add_player(player)


@router.post("/get_room_players/", tags=["room"],
            status_code=status.HTTP_200_OK,
            response_model=Union[list[Player], str])
async def get_room_players(room_id: RoomId,
                      rooms: Annotated[dict[str, Room], Depends(get_rooms)],
                      response: Response):
    room = rooms.get(room_id.room_id)
    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"no such room {room_id.room_id}"

    return list(room.players.values())


@router.put("/change_room_leader/", tags=["room"],
            status_code=status.HTTP_204_NO_CONTENT)
async def update_room_leader(update_leader: UpdateLeader,
                             rooms: Annotated[dict[str, Room], Depends(get_rooms)],
                             response: Response):
    room = rooms.get(update_leader.room_id.room_id)
    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "Room does not exist!"

    response_from_room = room.update_leader(player_id=update_leader.player_id.player_id,
                       new_leader_id=update_leader.new_leader_id.player_id)

    if response_from_room:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return response_from_room


@router.delete("/delete_room/", tags=["room"],
               status_code=status.HTTP_200_OK)
async def delete_room(room_id: RoomId,
                      rooms: Annotated[dict[str, Room], Depends(get_rooms)]):
    room = rooms.get(room_id.room_id)
    if not room:
        return

    rooms.pop(room.room_id)
