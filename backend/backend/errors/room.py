from fastapi import status, Request
from starlette.responses import JSONResponse


class PlayerNotInRoom(Exception):
    def __init__(self, players,*args):
        super().__init__(*args)
        self.players = players


class PlayerIsNotLeader(Exception):

    def __init__(self, player_name, *args):
        super().__init__(*args)
        self.player_name = player_name


async def player_is_not_leader_handler(request: Request,
                                       exc: PlayerIsNotLeader) -> JSONResponse:
    return JSONResponse(content={
        "message": f"player {exc.player_name} is not a room leader"
    },
        status_code=status.HTTP_409_CONFLICT
    )


async def player_not_in_room_handler(request: Request,
                                     exc: PlayerNotInRoom) -> JSONResponse:
    return JSONResponse(content={
        "message": f"play id's {exc.players} is not in room!"
    },
        status_code=status.HTTP_409_CONFLICT)