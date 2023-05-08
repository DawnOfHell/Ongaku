from fastapi import FastAPI

from .routes import room, player

app = FastAPI()
app.include_router(room.router)
app.include_router(player.router)
