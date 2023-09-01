from fastapi import APIRouter

router = APIRouter()


@router.post("/v1/user/new")
async def new_user():
    """
    Adds a new user to the database
    """
    pass
