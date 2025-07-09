from typing import Annotated
from fastapi import APIRouter, Depends, Header, HTTPException



async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
    
async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


### GLOBAL DEPENDENCIES ###

router = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)]) # In this case treat the router as if it were a FastAPI instance

### PATH OPERATION DEPENDENCIES ###
@router.get(
    "/items/dependencies/headers/",
    dependencies=[Depends(verify_token), Depends(verify_key)]
)
async def read_items_dependencies_headers():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]


