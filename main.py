from fastapi import FastAPI
from enum import Enum
import requestbody

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "test"}, {"item_name": "Bar"}]

app = FastAPI()
app.include_router(requestbody.router)

@app.get("/")
async def root():
    return { "message": "Hello world"}

# Path parameters and type conversion
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Predefined values: Working with Python enumerations
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}

# Path parameters containing paths
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# Query parameters
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# Optional query parameters
@app.get("/itemso/{item_id}")
async def read_one_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Query parameter type conversion #
# In this case short can be any variation of a boolean value, 
# such as "true", "yes", "1", etc.
@app.get("/items/type/{item_id}")
async def read_item_tc(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, 
    item_id: str, 
    q: str | None = None, 
    short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Required query parameters
# Declare a query parameter as required by not providing a default value.
@app.get("/items/required/{item_id}")
# Here, needy is a required query parameter
async def read_usr_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


### REQUEST BODY ###











# Project init

# def main():
#     print("Hello from eduread-microservices!")


# if __name__ == "__main__":
#     main()
