from datetime import datetime
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_database = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None
    
router = APIRouter()

@router.put("/item/json-compatible/{item_id}")
def update_item_json_compatible(item_id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_database[item_id] = json_compatible_item_data
    
