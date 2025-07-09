from typing import Annotated

from fastapi import APIRouter, Cookie
from pydantic import BaseModel

router = APIRouter()

class Cookies(BaseModel):
    model_config = {"extra": "forbid"} # Forbid extra cookies
    session_id: str
    facebook_tracker: str | None = None
    google_tracker: str | None = None
    
@router.get("/items/cookieparameters/")
async def read_items_cookies(
    cookies: Annotated[Cookies, Cookie()]
):
    return cookies