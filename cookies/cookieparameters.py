from typing import Annotated

from fastapi import APIRouter, Cookie

router = APIRouter()

@router.get("/items/cookieparameters/")
async def read_items_cookie(
    ads_id: Annotated[str | None, Cookie()] = None,
):
    return {"ads_id": ads_id}