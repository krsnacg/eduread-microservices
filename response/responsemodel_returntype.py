from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    
@router.post("/items/responsemodel_returntype/")
async def create_item(item: Item) -> Item:
    """
    This endpoint creates an item and returns it.
    The response model is specified as a return type.
    """
    return item

    
@router.get("/items/responsemodel_returntype/")
async def read_items_response_model() -> list[Item]:
    """
    This endpoint returns a list of items.
    The response model is specified as a return type.
    """
    return [
        Item(name="Foo", description="The pretender", price=42.0, tax=3.2, tags=["rock", "metal", "bar"]),
        Item(name="Bar", description="The bar", price=24.0, tax=1.5, tags=["jazz", "blues"]),
    ]
    
    
### response_model PARAMETER ###

@router.post("/items/responsemodel_parameter/", response_model=Item)
async def create_item_response_model(item: Item) -> Any:
    """
    This endpoint creates an item and returns it.
    The response model is specified as a parameter.
    """
    return item

@router.get("/items/responsemodel_parameter/", response_model=list[Item])
async def read_items_response_model_parameter() -> Any:
    """
    This endpoint returns a list of items.
    The response model is specified as a parameter.
    """
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
    
### Return the same input data ###

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

## This is not a good practice, but it is used here for demonstration purposes.
@router.post("/users/return_same_input_data/")
async def return_same_input_data(user: UserIn) -> UserIn:
    """
    This endpoint returns the same input data.
    The response model is specified as a return type.
    """
    return user

### Adding an output model to the response ###

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
@router.post("/users/return_output_model/", response_model=UserOut)
# If you declare the return type as UserOut, the editor will complain
# Instead use Any and response_model or use the alternative below (recommended)
async def return_output_model(user: UserIn) -> Any:
    return user


### RETURN TYPE AND DATA FILTERING ###

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
class UserRequest(BaseUser):
    password: str
    
# With this, we get tooling support, from editors and mypy as this code is correct 
# in terms of types, but we also get the data filtering from FastAPI.
@router.post("/users/return_type_and_data_filtering/")
async def create_user_return_type_and_data_filtering(
    user: UserRequest
) -> BaseUser:
    return user

### OTHER RETURN TYPE ANNOTATIONS ###

# Returning a response directly
from fastapi import Response
from fastapi.responses import JSONResponse, RedirectResponse

@router.get("/portal/response_directly/")
async def get_portal(teleport: bool = True) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal"})

# Annotate a response subclass

@router.get("/portal/response_subclass/")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# Invalid return type annotation
# This will fail
# @router.get("/portal/invalid_return_type/")
# async def get_invalid_return_type(teleport: bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here's your interdimensional portal."}

# Disabling Response Model
# This won¿t fail and FastAPI will skip the response model generation
@router.get("/portal/disable_response_model/", response_model=None)
async def get_disable_response_model(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

### RESPONSE MODEL ENCODING PARAMETERS ###

# if you have models with many optional attributes in a NoSQL database, 
# but you don't want to send very long JSON responses full of default values.
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

# the response (not including default values) will be:

# {
#     "name": "Foo",
#     "price": 50.2
# }

# But if your data has values for the model's fields with default values, like the item with ID bar:

# {
#     "name": "Bar",
#     "description": "The bartenders",
#     "price": 62,
#     "tax": 20.2
# }

# they will be included in the response.

@router.get("/items/response_model_encoding_parameters/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_item_response_model_encoding_parameters(item_id: str):
    return items[item_id]