import uuid
from typing import Annotated
from functools import lru_cache

from fastapi import APIRouter, Depends, status, HTTPException

from backend.api.models.player import Player

router = APIRouter(tags=["player"])


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

@router.post("/players/{player_name}",
             status_code=status.HTTP_202_ACCEPTED,
             response_model=Player)
async def create_player(player_name: str,
                        players: Annotated[dict[str, str], Depends(players)]):
    unique_id = f"{player_name}-{uuid.uuid4().hex[0:6]}"
    players.update({unique_id: player_name})
    return Player(player_id=unique_id, player_name=player_name)


@router.delete("/players/{player_id}",
               status_code=status.HTTP_200_OK)
async def delete_player(players: Annotated[dict[str, str], Depends(players)],
                        player: Annotated[Player, Depends(get_player_by_id)]):
    return players.pop(player.player_id)
