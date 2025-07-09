from fastapi import FastAPI, Path, Query, APIRouter
from typing import Annotated

router = APIRouter()

@router.get("/items/validation/{item_id}")
# A path parameter is always required, even if it has a default value or None type.
async def read_item_validation(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(max_length=50)] = None
):
    results: dict[str, object] = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


### NUMBER VALIDATION ###

@router.get("/items/numbervalidation/{item_id}")
async def read_item_number(
    item_id: Annotated[int, Path(ge=1, title="The ID of the item to get")],
    q: Annotated[str | None, Query(max_length=50)] = None
):
    results: dict[str, object] = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
# numeric validations:
# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal

### FLOAT VALIDATION ###

@router.get("/items/floatvalidation/{item_id}")
async def read_item_float(
    *,
    item_id: Annotated[int, Path(title="The ID  of the item to get", ge=0, le=100)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)]
):
    results: dict[str, object] = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results