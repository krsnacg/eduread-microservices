from typing import Annotated

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

router = APIRouter()

class Item(BaseModel):
    # Field additional arguments
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])
    
    # Extra JSON Schema data in Pydantic models
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            ]
        }
    }
    
### BODY WITH EXAMPLES ###

# This example considers the Item model as without the Field and model config extra examples

@router.put("/items/bodywithexamples/{item_id}")
async def update_item(
    item_id: int, 
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                },
                                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ]
        )
    ]
):
    return {"item_id": item_id, "item": item}