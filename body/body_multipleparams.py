from typing import Annotated

from fastapi import FastAPI, APIRouter, Path, Query, Body
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
### MIXING PATH, QUERY, AND BODY PARAMETERS ###

@router.put("/items/mixing/{item_id}")
async def update_item_mixing(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)], 
    q: str | None = None,
    item: Item | None = None, # Adding None as default allows body to be optional
):
    result: dict[str, object] = {"item_id": item_id}
    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item})
    return result

### MULTIPLE BODY PARAMETERS ###

class User(BaseModel):
    username: str
    full_name: str | None = None

@router.put("/items/multiplebodies/")
async def update_item_multiplebody(item_id: int, item: Item, user: User):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user
    }
    return results

### SINGULAR VALUES IN BODY ###

@router.put("/items/singularbody/")
async def update_item_singular(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
    return results

### MULTIPLE BODY PARAMS AND QUERY ###

# Basically the same as the previous examples, but with an additional query parameter.

@router.put("/items/multiplebodyquery/")
async def update_item_multiplebody_query(
    item_id: int, 
    item: Item, 
    user: User, 
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
    }
    if q:
        results.update({"q": q})
    return results


### EMBED A SINGLE BODY PARAMETER ###
# Basically makes the body parameter a single object that is embedded in the request body.
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }
@router.put("/items/embedbody/")
async def update_item_embed(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results: dict[str, object] = {"item_id": item_id, "item": item}
    return results