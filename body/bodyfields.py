from typing import Annotated
from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300, min_length=10
    )
    price: float = Field(gt=0, description="The price must be greater than 0")
    tax: float | None = None
    
@router.put("/items/bodyfields/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    """
    Update an item with the given item_id.
    The item data is provided in the request body.
    """
    return {"item_id": item_id, "item": item}