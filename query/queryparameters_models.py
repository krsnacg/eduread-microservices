from fastapi import FastAPI, APIRouter, Query
from pydantic import BaseModel, Field
from typing import Annotated, Literal

router = APIRouter()

### Query Parameters with a Pydantic Model ###

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
    
@router.get("/items/queryparammodels/")
async def read_items_queryparammodels(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


### Forbid Extra Query Parameters ###

class FilterParamsNoExtra(BaseModel):
    model_config = {"extra": "forbid"}
    
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
    
@router.get("/items/queryparammodels/noextra/")
async def read_items_queryparammodels_noextra(
    filter_query: Annotated[FilterParamsNoExtra, Query()]
):
    return filter_query
