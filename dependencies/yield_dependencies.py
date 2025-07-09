from typing import Annotated

from fastapi import Depends

class DepA:
    pass

class DepB:
    pass

def generate_dep_a():
    return "Dependency A"

def generate_dep_b():
    return "Dependency B"

def generate_dep_c():
    return "Dependency C"

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        print(f"Cleaning up {dep_a}")
        
async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        print(f"Cleaning up {dep_b} with {dep_a}")
        
async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        print(f"Cleaning up {dep_c} with {dep_b}")
        
        
### Dependencies with yield and HTTPException ###

from fastapi import HTTPException, APIRouter

router = APIRouter()

data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}

class OwnerError(Exception):
    pass

def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=400, detail=f"Owner error: {e}")
    
@router.get("/items/yield/{item_id}")
async def read_item_yield(
    item_id: str, 
    username: Annotated[str, Depends(get_username)]
):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = data[item_id]
    
    if item["owner"] != username:
        raise OwnerError(username)
    return item

### Always raise in Dpenendencies with yield and except ###

class InternalError(Exception):
    pass

def get_username_always_raise():
    try:
        yield "Rick"
    except InternalError:
        print("We don't swallow the internal error, we always raise it")
        raise
    

### CONTEXT MANAGERS ###

class MySuperContextManager:
    def __init__(self):
        print("Initializing db connection or similar")
        
    def __enter__(self):
        print("Entering MySuperContextManager")
        return "Returning the db connection or similar"
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing the db connection or similar")
    
    
async def get_db():
    with MySuperContextManager() as db:
        yield db
    