from typing import Annotated, Any
from fastapi import Depends, APIRouter

router = APIRouter()

# FastAPI can accept any dependency as long as it is callable.
# This includes functions, classes, and even async functions.

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
        
@router.get("/items/class/dependencies/")
async def read_items_class_dependencies(commons: Annotated[Any, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response["q"] = commons.q
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

### Shortcut for the same functionality ###
@router.get("/items/shortcut/dependencies/")
async def read_items_shortcut_dependencies(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response["q"] = commons.q
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

