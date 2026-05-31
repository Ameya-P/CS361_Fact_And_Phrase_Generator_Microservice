from db import connect_to_db
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, HTTPException
from models import PhraseRequest, PhraseResponse
from typing import Annotated, Literal
from bson.objectid import ObjectId
import bson.errors

collection = None

@asynccontextmanager
async def lifespan(app):
    # startup code
    global collection 
    collection = connect_to_db()
    yield
    # shutdown code
    pass

app = FastAPI(lifespan=lifespan)

# ---- Define Routes Here ----
""" 
Notes on how to implement it:
- The function needs to be async
- FastAPI declares query parameters by adding them as function arguments. We have a Pydantic model for the request. How FastAPI handles query parameters from a model using Query (https://fastapi.tiangolo.com/tutorial/query-param-models/)
- Motor's find_one takes a filter dict as the first argument?
- Sorting by num_uses ascending before grabbing one result. Motor has a sort method. """


@app.get("/phrase/")
async def get_phrase(filter_query: Annotated[PhraseRequest, Query()]):
    """
    Gets a phrase and filters by category if provided.
    Call update_num_uses after getting a phrase.
    Returns least used phrase.
    """
    try:
        # filter by category when provided; otherwise search across all phrases
        query = {}

        if filter_query.category:
            query["category"] = filter_query.category

        phrase = await collection.find_one(query, sort=[("num_uses", 1)])
    except Exception:
        raise HTTPException(status_code=500, detail="Could not connect to database.")

    # error handling for when there is no phrase found in the query category 
    if phrase is None:
        if filter_query.category:
            raise HTTPException(status_code=404, detail=f"There are no phrases found for the category: {filter_query.category}.")

        # when there is no phrase within the database (for user story 1 where the microservice selects the fact with the lowest num_uses value.)
        raise HTTPException(status_code=404, detail="There are no phrases found in the database.")
    else:
        await update_num_uses(phrase["_id"])

    # if ObjectId is not automatically jsonifiable
    phrase["_id"] = str(phrase["_id"])

    return phrase


@app.patch("/phrase/")
async def update_num_uses(phrase_id: str):
    """
    Update num_uses by 1 after getting a phrase.
    """

    # error handling for incorrect phrase_ids 
    try:
        object_id = ObjectId(phrase_id)
    except bson.errors.InvalidId:
        raise HTTPException(status_code=400, detail=f"Conversion failed. Invalid ID format: {phrase_id}")

    updated = await collection.update_one({"_id" : object_id}, {"$inc": {"num_uses": 1}})

    # error for when the input phrase_id is valid but not found within the database.
    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"There is no phrase found in the database with the phrase ID: {phrase_id}.")
    
    # if the phrase is found but no changes are made
    if updated.modified_count != 1:
        raise HTTPException(status_code=500, detail=f"The phrase with the phrase ID: {phrase_id} has been found but its num_uses has not been updated.")

    # return the matched and modified count number. 
    return { 
        "phrase_id" : phrase_id,
        "updated.matched_count: " : updated.matched_count, 
        "updated.modified_count: " : updated.modified_count
        }


