from fastapi import APIRouter

router = APIRouter()


@router.post("/v1/user/new")
async def new_user():
    """
    Adds a new user to the database
    """
    pass


@router.post("/v1/user/{user_id}/delete")
async def delete_user():
    pass


@router.post("/v1/user/{user_id}/login")
async def login():
    pass
