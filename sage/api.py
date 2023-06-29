from typing import Sequence

from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sage.main import add_new_round
from sage.utils.types import CourseHandicapRequest, PlayingHandicapRequest, Round

app = FastAPI()


class ScorecardRequest(BaseModel):
    images: Sequence[UploadFile]


@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})


@app.post("/user/new")
async def new_user():
    """
    Adds a new user to the database
    """
    pass


@app.get("/user/{user_id}/handicap-index")
async def get_user_handicap(user_id: str):
    pass


@app.get("/user/{user_id}/course-handicap")
async def get_course_handicap(user_id: str, request: CourseHandicapRequest):
    pass


@app.get("/user/{user_id}/playing-handicap")
async def get_playing_handicap(user_id: str, request: PlayingHandicapRequest):
    pass


@app.post("/user/{user_id}/round/new")
async def add_round(user_id: str, round: Round):
    """
    Manually add a new round to the database.
    """
    message, status_code = add_new_round(user_id, round)
    return JSONResponse(content={"message": message}, status_code=status_code)


@app.post("/user/{user_id}/round/new/scorecard")
async def upload_scorecard(user_id: str, request: ScorecardRequest):
    """
    Allows a user to input a sequence of scorecards to add to
    their database
    """
    pass


@app.put("/user/{user_id}/round/{round_id}/update")
async def update_round(user_id: str, round_id: str):
    """
    Make changes to an existing round
    """
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("sage.api:app", host="localhost", port=8002, reload=True)
