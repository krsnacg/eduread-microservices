from fastapi import FastAPI, HTTPException

router = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@router.get("/items/error/{item_id}")
async def read_item_error(item_id: str):
    if item_id not in items:
        # This will terminate the request at this point and return a 404 error
        raise HTTPException(status_code=404, detail="Item not found") # detail can be dict, list, etc
    return {"item": items[item_id]}


### ADD CUSTOM HEADERS ###
@router.get("/items/custom-header/{item_id}")
async def read_item_custom_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, 
            detail="Item not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}


### INSTALL CUSTOM EXCEPTION HANDLER ###
from fastapi import Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
        

@router.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,  # HTTP status code for "I'm a teapot"
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


### OVERRIDE THE DEFAULT EXCEPTION HANDLERS ###

# Override request validation exceptions

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

@router.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

# Now, if you go to /items/foo, instead of getting the default JSON error with:
# {
#     "detail": [
#         {
#             "loc": [
#                 "path",
#                 "item_id"
#             ],
#             "msg": "value is not a valid integer",
#             "type": "type_error.integer"
#         }
#     ]
# }

# you will get a text version, with:

# 1 validation error
# path -> item_id
#   value is not a valid integer (type=type_error.integer)

# Override the HTTPException error handler
from pydantic import BaseModel
from fastapi.exceptions import HTTPException as StarletteHTTPException

@router.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@router.get("/items/validation-error/{item_id}")
async def read_item_validation_error(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3")
    return {"item_id": item_id}


### Use the RequestValidationError body ###

from fastapi.encoders import jsonable_encoder

@router.exception_handler(RequestValidationError)
async def validation_exception_handler_body(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )
    
class Item(BaseModel):
    title: str
    size: int
    
@router.post("/items/validation-error-body/")
async def create_item_validation_error_body(item: Item):
    return item

# sending an invalid item like:

# {
#   "title": "towel",
#   "size": "XL"
# }

# will return a response telling you that the data is invalid containing the received body:

# {
#   "detail": [
#     {
#       "loc": [
#         "body",
#         "size"
#       ],
#       "msg": "value is not a valid integer",
#       "type": "type_error.integer"
#     }
#   ],
# # #   "body": {
# # #     "title": "towel",
# # #     "size": "XL"
# # #   }
# }

### REUSE FASTAPI'S EXCEPTION HANDLERS ###
from fastapi.exception_handlers import (
    # http_exception_handler, ## Uncomment this, and delete the custom handler defined above
    request_validation_exception_handler,
)


@router.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@router.exception_handler(RequestValidationError)
async def validations_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}