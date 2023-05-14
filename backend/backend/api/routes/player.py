import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.api.models.player import Player
from backend.api.dependencies.player import players, get_player_by_id

router = APIRouter(tags=["player"])


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
def delete_player(players: Annotated[dict[str, str], Depends(players)],
                        player: Annotated[Player, Depends(get_player_by_id)]):
    return players.pop(player.player_id)
