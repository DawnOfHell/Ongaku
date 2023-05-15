from typing import Annotated
from functools import lru_cache

from fastapi import status, HTTPException, Depends, Body

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


def get_player_by_id_body(player_id: Annotated[str, Body(embed=True)],
                          players: Annotated[dict[str, str], Depends(players)]):
    return get_player_by_id(player_id, players)


def get_other_by_id(other_id: Annotated[str, Body(embed=True)],
                    players:Annotated[dict[str, str], Depends(players)]):
    player = players.get(other_id)

    if not player:
        raise HTTPException(detail=f"player {other_id} does not exist!",
                            status_code=status.HTTP_404_NOT_FOUND)
    return Player(player_id=other_id, player_name=player)
