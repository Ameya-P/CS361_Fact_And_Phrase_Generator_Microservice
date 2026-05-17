# CS361_Fact_And_Phrase_Generator_Microservice
## Description
This microservice accesses a database of facts and phrases stored on MongoDB. Client programs can make API requests to the service to receive either a random string from the entire database or a random string from within a specific category within the database. The microservice counts the number of times each string has been returned and prioritizes those that have been returned less often.

## Requesting Data
Clear instructions for how to programmatically REQUEST data from the microservice. Include an example call.

## Receiving Data
Clear instructions for how to programmatically RECEIVE data from the microservice. Include an example call.

## UML Sequence Diagram
Show how requesting and receiving data works. Make it detailed enough that your teammates (and your grader) will understand.

![Sequence Diagram](Fact_and_Phrase_Generator_Microservice.png)


# Below this heading -- all the previous content Ameya added. should be deleted at some point
## Technologies Used

### Uvicorn
Server that runs our FastAPI app. Listen for incoming connections and serve traffic.

### Motor
Python driver that runs the query against our MongoDB database and hands back the result. It's async so our service can handle other requests while it's waiting on MongoDB to respond rather than being blocked.

### FastAPI
Light weight async-native web framework that handles incoming HTTP requests and routes them to our functions.

HTTP request → Uvicorn → FastAPI (routing) → Motor (query MongoDB) → Pydantic (shape the response) → HTTP response

### Render
Hosts the service. 

### Github Actions
CI/CD pipeline. 

push to main → Actions runs tests → if tests pass → Render auto-deploys

## File Explanations

### main.py
Where the routes live.

### models.py
Defines Pydantic models (specifically the shape and types of our requests and responses).

### db.py
Establishes the db connection.

### test_main.py
Contains integration tests. Seed data can be found in seed_data.py.
