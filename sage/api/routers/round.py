from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from sage.main import add_new_round
from sage.models.golf import Hole, Round, Rounds
from sage.models.requests import StartRoundRequest
from sage.models.responses import RoundsResponse
from sage.utils.logging import get_logger
from sage.utils.settings import Settings

router = APIRouter()
settings = Settings()
logger = get_logger(settings.log_level)
rounds: Rounds = {}


@router.get("/v1/user/{user_id}/rounds")
async def get_rounds(user_id: str):
    return RoundsResponse(rounds=[round.to_key_data() for round in rounds.values()])


@router.post("/v1/user/{user_id}/round/new")
async def add_round(user_id: str, round: Round):
    """
    Manually add a new round to the database.
    """
    message, status_code = add_new_round(user_id, round)
    return JSONResponse(content={"message": message}, status_code=status_code)


@router.post("/v1/user/{user_id}/round/start")
async def start_round(user_id: str, new_round: StartRoundRequest):
    """
    Start a new round.
    """
    try:
        round = Round.from_request(new_round)
        rounds[round.id] = round
        message = "Round added"
        status_code = 200
        round_id = round.id
    except Exception as exc:
        logger.error(f"Unable to parse round object: {exc}")
        message = f"Error: {exc}"
        status_code = 400
        round_id = None
    return JSONResponse(
        content={"message": message, "round_id": round_id}, status_code=status_code
    )


@router.put("/v1/user/{user_id}/round/{round_id}/update")
async def update_hole(user_id: str, round_id: str, data: Hole):
    """
    Add data for a hole
    """
    score = await rounds[round_id].update(data)
    return score
