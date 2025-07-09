from fastapi import APIRouter

router = APIRouter()

@router.post("/items/response_status_code/", status_code=201)
async def create_item_response_status_code(name: str):
    return {"name": name}


### SHORTCUT TO REMEMBER STATUS NAMES

from fastapi import status

@router.post("/items/response_status_code_shortcut/", status_code=status.HTTP_201_CREATED)
async def create_item_response_status_code_shortcut(name: str):
    return {"name": name}

