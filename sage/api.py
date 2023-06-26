from typing import Sequence

from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class ScorecardRequest(BaseModel):
    images: Sequence[UploadFile]


@app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})


@app.post("/new/user")
async def new_user():
    """
    Adds a new user to the database
    """
    pass


@app.post("/{user_id}/scorecard")
async def upload_scorecard(user_id: str, request: ScorecardRequest):
    """
    Allows a user to input a sequence of scorecards to add to
    their database
    """
    pass


@app.post("/{user_id}/round")
async def add_round(user_id: str):
    """
    Manually add a new round to the database.
    """
    pass


@app.put("/{user_id}/{round_id}/update")
async def update_round(user_id: str, round_id: str):
    """
    Make changes to an existing round
    """
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("sage.api:app", host="localhost", port=8002, reload=True)
