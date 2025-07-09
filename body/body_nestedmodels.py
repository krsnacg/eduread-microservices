from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

router = APIRouter()

### LIST FIELDS ###

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []
    
    
### LIST FIELDS WITH TYPE PARAMETERS ###

class ItemListType(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []  # List of strings
    
    
### SET TYPES ###
class ItemSetType(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()  # Set of strings
    

### NESTED MODELS ###

# FastAPI expects a model like the following:
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": ["rock", "metal", "bar"],
#     "image": {
#         "url": "http://example.com/baz.jpg",
#         "name": "The Foo live"
#     }
# }


class Image (BaseModel):
    url: HttpUrl # Special type
    name: str

class ItemNestedModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None  # Nested model
    
@router.put("/items/nestedmodels/")
async def update_item_nested(item_id: int, item: ItemNestedModel):
    """
    Create an item with nested model.
    """
    return {"item_id":item_id, "item": item}

### Attributes with lists of submodels ###

# FastAPI expects a model like the following:
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": [
#         "rock",
#         "metal",
#         "bar"
#     ],
#     "images": [
#         {
#             "url": "http://example.com/baz.jpg",
#             "name": "The Foo live"
#         },
#         {
#             "url": "http://example.com/dave.jpg",
#             "name": "The Baz"
#         }
#     ]
# }

class ItemWithSubmodels(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: list[Image] | None = None  # List of submodels
    
    
### DEEPLY NESTED MODELS ###
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[ItemWithSubmodels]  # List of items with submodels

@router.post("/offers/")
async def create_offer(offer: Offer):
    """
    Create an offer with deeply nested models.
    """
    return offer


### BODIES OF PURE LISTS ###

@router.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    """
    Create multiple images.
    """
    return images

### BODIES OF ARBITRARY DICTS ###

@router.post("/index-weights/")
async def create_index_weights(index_weights: dict[str, float]):
    """
    Create index weights.
    """
    return index_weights