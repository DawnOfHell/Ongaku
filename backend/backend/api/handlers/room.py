from fastapi import status, Request
from starlette.responses import JSONResponse

from backend.errors.room import PlayerNotInRoomError, PlayerIsNotLeaderError


async def player_is_not_leader_handler(request: Request,
                                       exc: PlayerIsNotLeaderError) -> JSONResponse:
    return JSONResponse(content={
        "message": f"player {exc.player_name} is not a room leader"
    },
        status_code=status.HTTP_409_CONFLICT
    )


async def player_not_in_room_handler(request: Request,
                                     exc: PlayerNotInRoomError) -> JSONResponse:
    return JSONResponse(content={
        "message": f"play id's {exc.players} is not in room!"
    },
        status_code=status.HTTP_409_CONFLICT)