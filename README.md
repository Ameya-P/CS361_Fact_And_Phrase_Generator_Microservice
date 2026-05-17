# CS361_Fact_And_Phrase_Generator_Microservice
## Description
This microservice accesses a database of facts and phrases stored on MongoDB. Client programs can make API requests to the service to receive either a random string from the entire database or a random string from within a specific category within the database. The microservice counts the number of times each string has been returned and prioritizes those that have been returned less often.

## Requesting Data
To request a fact or phrase, make an HTTP GET request to the /phrase/ endpoint. You can append an optional category query parameter to filter the results. If no category is provided, it retrieves the least-used phrase across all categories.
Example call: Will need the Render url where it is hosted

You can simply paste either of these urls into your address bar to quickly test the application:
https://cs361-fact-and-phrase-generator.onrender.com/phrase/?category=space
https://cs361-fact-and-phrase-generator.onrender.com/phrase/

Or programmatically (python):

import requests
# Request a phrase from the 'space' category
response = requests.get("https://cs361-fact-and-phrase-generator.onrender.com/phrase/?category=space")

## Receiving Data
Once you have received a response, you can parse the phrase from the json file. You can also simply view the entire JSON object as seen below (python):

data = response.json()
print(data)

The resulting output should look similar to this:
{
  "_id": "64abcdef1234567890",
  "title": "Massive Sun",
  "phrase": "The sun makes up more than 99 percent of the mass in our solar system.",
  "category": "space",
  "num_uses": 1
}

If there are no facts for that category, you will receive this:
{
  "detail": "There are no phrases found for the category: Biolog."
}

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
