from typing import Annotated

from fastapi import APIRouter, Header

router = APIRouter()

@router.get("/items/headerparameters/")
async def read_items_header(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}


### DUPLICATE HEADERS ###
@router.get("/items/duplicateheaders/")
async def read_items_duplicate(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}