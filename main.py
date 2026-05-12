from db import connect_to_db
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from models import PhraseRequest, PhraseResponse
from typing import Annotated, Literal

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
    '''
    Gets a phrase and filters by category if provided. 
    Call update_num_uses after getting a phrase.
    Returns least used phrase. 
    '''
    pass

@app.patch("/phrase/")
async def update_num_uses(filter_query: Annotated[PhraseRequest, Query()]):
    '''
    Update num_uses by 1 after getting a phrase.
    '''
    pass