from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter()

# class UserRequest(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None
    
# class UserResponse(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
    
# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: str | None = None
    
# def fake_hash_password(password: str):
#     return "supersecret" + password

# def fake_save_user(user: UserRequest):
#     # Simulate saving the user to a database
#     hashed_password = fake_hash_password(user.password)
#     user_in_db = UserInDB(**user.model_dump(), hashed_password=hashed_password)
#     print("User saved! ...testing purposes only")
#     return user_in_db


# @router.post("/users/create/", response_model=UserResponse)
# async def create_user(user: UserRequest):
#     user_saved = fake_save_user(user)
#     return user_saved


### BETTER APPROACH ###

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@router.post("/user/create", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


### Union or anyOf ###

from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str
    
    
class CarItem(BaseModel):
    type: str = "car"

class PlaneItem(BaseModel):
    type: str = "plane"
    size: int
    
items_union = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@router.get("/items/union/{item_id}", response_model=Union[CarItem, PlaneItem])
async def read_item_union(item_id: str):
    return items_union[item_id]

### LIST OF MODELS ###

class Item(BaseModel):
    name: str
    description: str
    
items_list = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@router.get("/items/list", response_model=list[Item])
async def read_items_list():
    return items_list


### RESPONSE WITH ARBITRARY DICT ###

@router.get("/items/arbitrary_dict", response_model=dict[str, float])
async def read_items_arbitrary_dict():
    return {"item1": 42.0, "item2": 24.0, "item3": 12.5}