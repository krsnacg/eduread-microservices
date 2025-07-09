from typing import Annotated

from fastapi import APIRouter, Depends

router = APIRouter()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@router.get("/items/dependency/")
async def read_items_dependency(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@router.get("/users/dependency/")
async def read_users_dependency(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

### Share Annotated Dependencies ###

CommonsDep = Annotated[dict, Depends(common_parameters)]

@router.get("/items/dependency/annotated/")
async def read_items_dependency_annotated(commons: CommonsDep):
    return commons

@router.get("/users/dependency/annotated/")
async def read_users_dependency_annotated(commons: CommonsDep):
    return commons