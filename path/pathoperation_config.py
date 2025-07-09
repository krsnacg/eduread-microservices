from fastapi import APIRouter, status
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

router = APIRouter()

# parameters that you can pass to the path operation decorator

@router.post("/items/", status_code=status.HTTP_201_CREATED, response_model=Item)
async def create_item_response(item: Item):
    return item

### TAGS ###

@router.post("/items/tags/", tags=["items"], response_model=Item)
async def create_item_tags(item: Item):
    return item

### TAGS WITH ENUMS ###

from enum import Enum

class Tags(Enum):
    items = "items"
    users = "users"
    
    
@router.get("/items/tags-enum/", tags=[Tags.items])
async def get_items_tags_enum():
    return ["Portal gun", "Plumbus"]


### SUMMARY AND DESCRIPTION ###
@router.post(
    "/items/summary-description/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with a name, description, price, tax, and tags.",
)
async def create_item_summary_description(item: Item):
    return item

### DESCRIPTION FROM DOCSTRING ###
@router.post("/items/description-docstring/", response_model=Item, summary="Create an item with a docstring description")
async def create_item_description_docstring(item: Item):
    """
    Create an item with a name, description, price, tax, and tags.
    
    This endpoint allows you to create an item with the specified attributes.
    The `name` is required, while `description`, `tax`, and `tags` are optional.
    
    - **name**: The name of the item (required).
    - **description**: A brief description of the item (optional).
    - **price**: The price of the item (required).
    - **tax**: The tax applied to the item (optional).
    - **tags**: A set of tags associated with the item (optional).
    """
    return item


### RESPONSE DESCRIPTION ###
@router.post(
    "/items/response-description/",
    response_model=Item,
    response_description="The created item with its details.",
    status_code=status.HTTP_201_CREATED,
    summary="Create an item with a response description",
)
async def create_item_response_description(item: Item):
    """
    Create an item with a name, description, price, tax, and tags.
    
    This endpoint allows you to create an item with the specified attributes.
    The `name` is required, while `description`, `tax`, and `tags` are optional.
    
    - **name**: The name of the item (required).
    - **description**: A brief description of the item (optional).
    - **price**: The price of the item (required).
    - **tax**: The tax applied to the item (optional).
    - **tags**: A set of tags associated with the item (optional).
    """
    return item

### DEPRECATE A PATH OPERATION ###
@router.get("/items/deprecated/element", tags=["items"], deprecated=True)
async def get_deprecated_item():
    return [{"item_id": "Foo"}]