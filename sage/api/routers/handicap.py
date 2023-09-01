from fastapi import APIRouter

from sage.utils.types import CourseHandicapRequest, PlayingHandicapRequest

router = APIRouter()


@router.get("/v1/user/{user_id}/handicap-index")
async def get_user_handicap(user_id: str):
    pass


@router.get("/v1/user/{user_id}/course-handicap")
async def get_course_handicap(user_id: str, request: CourseHandicapRequest):
    pass


@router.get("/v1/user/{user_id}/playing-handicap")
async def get_playing_handicap(user_id: str, request: PlayingHandicapRequest):
    pass
