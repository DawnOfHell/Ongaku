from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from .routes import room, player

app = FastAPI()
app.include_router(room.router)
app.include_router(player.router)
app.add_exception_handler(HTTPException, handler=http_exception_handler)