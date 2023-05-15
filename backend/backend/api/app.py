from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from .routes import room, player
from backend.api.handlers import room as room_errors

app = FastAPI()
app.include_router(room.router)
app.include_router(player.router)
app.add_exception_handler(HTTPException,
                          handler=http_exception_handler)
app.add_exception_handler(room_errors.PlayerNotInRoom,
                          handler=room_errors.player_not_in_room_handler)
app.add_exception_handler(room_errors.PlayerIsNotLeader,
                          handler=room_errors.player_is_not_leader_handler)
