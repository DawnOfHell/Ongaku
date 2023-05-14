from typing import Annotated
from functools import lru_cache

from fastapi import status, HTTPException, Depends

from backend.api.models.player import Player


@lru_cache
def players() -> dict[str, str]:
    return {}


def get_player_by_id(player_id: str,
                     players: Annotated[dict[str, str], Depends(players)]):
    player = players.get(player_id)
    if not player:
        raise HTTPException(detail=f"player {player_id} does not exist!",
                             status_code=status.HTTP_404_NOT_FOUND)
    return Player(player_id=player_id, player_name=player)


def get_other_by_id(other_id:str,
                    players:Annotated[dict[str, str], Depends(players)]):
    player = players.get(other_id)

    if not player:
        raise HTTPException(detail=f"player {other_id} does not exist!",
                            status_code=status.HTTP_404_NOT_FOUND)
    return Player(player_id=other_id, player_name=player)