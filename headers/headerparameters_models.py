from typing import Annotated

from fastapi import APIRouter, Header
from pydantic import BaseModel

router = APIRouter()

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}  # Forbid extra headers
    
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
    
@router.get("items/headerparameters/")
async def read_items_header(headers: Annotated[CommonHeaders, Header()]):
    return headers