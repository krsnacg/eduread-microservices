from typing import Annotated
from fastapi import APIRouter, Cookie, Depends

router = APIRouter()

def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: Annotated[str | None, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None
):
    if not q:
        return last_query
    return q

@router.get("/items/query/cookie/dependencies/")
async def read_items_query_cookie_dependencies(
    query_or_default: Annotated[str | None, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}

