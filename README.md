# CS361_Fact_And_Phrase_Generator_Microservice

## FastAPI
Light weight async-native web framework that handles incoming HTTP requests and routes them to our functions.

# Motor
Python driver that runs the query against our MongoDB database and hands back the result. It's async so our service can handle other requests while it's waiting on MongoDB to respond rather than being blocked.

# Uvicorn
Server that runs our FastAPI app. Listen for incoming connections and serve traffic.


## File Explanations

### main.py
Where the routes live.

### models.py
Defines Pydantic models (specifically the shape and types of our requests and responses)

## db.py
Establishes the db connection

## test_main.py
Contains integration tests. Seed data can be found in seed_data.py