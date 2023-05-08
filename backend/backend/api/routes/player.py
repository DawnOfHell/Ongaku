import uuid
from typing import Annotated
from functools import lru_cache

from fastapi import APIRouter, Depends, status

from backend.api.models.player import PlayerId, PlayerName

router = APIRouter()


@lru_cache
def get_players() -> dict:
    return {}


@router.post("/create_player/", tags=["player"],
             status_code=status.HTTP_202_ACCEPTED,
             response_model=PlayerId)
async def create_player(player_name: PlayerName,
                        players: Annotated[dict[str, str], Depends(get_players)]):
    unique_id = f"{player_name.player_name}-{uuid.uuid4().hex[0:6]}"
    players.update({unique_id: player_name.player_name})
    return PlayerId(player_id=unique_id)


@router.delete("/delete_player", tags=["player"],
               status_code=status.HTTP_200_OK)
async def delete_player(player_id: PlayerId,
                        players: Annotated[dict[str, str], Depends(get_players)]):
    player = players.get(player_id.player_id)

    if not player:
        return

    players.pop(player_id.player_id)
