from db import connect_to_db
from contextlib import asynccontextmanager
from fastapi import FastAPI

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