import random
from fastapi import APIRouter

### libraries needed for validation ###
from fastapi import Query
from typing import Annotated

### libraries needed for custom validation ###
from pydantic import AfterValidator

router = APIRouter()


### ENFORCE ADDITIONAL VALIDATION ###
@router.get("/items/validate/")
async def read_items_val(q: Annotated[str | None, Query(min_length=3,max_length=50)] = None):
    results: dict[str, object] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


### ADDING REGULAR EXPRESSIONS ###
# This specific regular expression pattern checks that the received parameter value:
#     ^: starts with the following characters, doesn't have characters before.
#     fixedquery: has the exact value fixedquery.
#     $: ends there, doesn't have any more characters after fixedquery.

@router.get("/items/regex/")
async def read_items_regex(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results: dict[str, object] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Having a default value of any type, including None, 
# makes the parameter optional (not required).

### REQUIRED CAN BE NONE ###

@router.get("/items/none/")
async def read_items_reqnone(q: Annotated[str | None, Query(min_length=3)]):
    results: dict[str, object] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

### QUERY PARAMETER LIST / MULTIPLE VALUES ###
# Can be used to receive multiple values for the same query parameter.
# i.e. http://localhost:8000/items/list/?q=foo&q=bar
@router.get("/items/list/")
async def read_items_querylist(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


### DECLARE MORE METADADA ###

@router.get("/items/metadata/")
async def read_items_metadata(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3
        ),
    ] = None,
):
    results: dict[str, object] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


### ALIAS PARAMETERS ###

@router.get("/items/alias/")
async def read_items_alias(
    q: Annotated[str | None, Query(alias="item-query")] = None
):
    results: dict[str, object] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

### DEPRECATED PARAMETERS ###

@router.get("/items/deprecated/")
async def read_items_deprecated(
    q: Annotated[
        str | None, 
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        )
    ] = None
):
    results: dict[str, object] = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


### CUSTOM VALIDATION ###
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str) -> str:
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format, must start with 'isbn-' or 'imdb-'")
    return id

@router.get("/items/custom/")
async def read_items_custom(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
        
    return {"id": id, "item": item}