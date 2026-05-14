"""
- pytest works by looking for functions that start with test_
    and running them automatically.
- assert the result. If the expression after it is True, the test passes.
    If it's False, the test fails with a clear error message.

Example Test

def test_something():
    result = 2 + 2
    assert result == 4

FastAPI ships with a built-in TestClient

response = client.get("/phrase/")
assert response.status_code == 200
"""

import pytest
from pymongo import MongoClient
from unittest.mock import patch
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import motor.motor_asyncio
import main
from main import app
from seed_data import seed_data_list

load_dotenv()


def connect_to_test_db():
    MONGO_URI = os.getenv('MONGO_URI')
    client = MongoClient(MONGO_URI)
    db = client["test-microservices"]
    collection = db["test-fact-or-phrase-generator"]
    return collection


# added this because testing needs to target the test database, not
#   the production one. This way, the connect_to_db function from db.py
#   can be swapped out for testing purposes.
def override_connect_to_db():
    MONGO_URI = os.getenv('MONGO_URI')
    async_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    return async_client["test-microservices"]["test-fact-or-phrase-generator"]


# Perform the swap so that when FastAPI runs the startup sequence
#   for the app, the lifespan function uses a different function to
#   connect to the database. This way we are ensuring we connect to a
#   test database, not the production one
main.connect_to_db = override_connect_to_db


@pytest.fixture
def seed_data():
    test_collection = connect_to_test_db()
    test_collection.insert_many([document.copy() for document in seed_data_list])
    yield test_collection
    test_collection.drop()


# global variable for TestClient used to be here, no longer because it prevented
#   us from running multiple GETs within the same test. The client would run once
#   but then it would pass the yield statement in the lifespan function in main,
#   causing app to be killed. This is fixed with "with" blocks below.

# --- Tests -----


def test_no_category(seed_data):
    """
    Tests to ensure data can be retrieved at all
    Tests to ensure num_uses is updated by main.py after a GET
    Tests to ensure lowest num_uses entry is always retrieved
    """
    # Using a with block forces the app to run its startup sequence
    # and stay open for the entire duration of this block
    with TestClient(app) as client:
        response1 = client.get("/phrase/")
        # did we get a response at all?
        assert response1.status_code == 200
        data1 = response1.json()

        response2 = client.get("/phrase/")
        assert response2.status_code == 200
        data2 = response2.json()
        # make sure num_uses was updated from 0 to 1 because we got the same entry as last time
        assert data2['num_uses'] == 1

        # seed_data has been modified so that the first entry is far behind
        #   on num_uses and must be selected again.
        assert data1["_id"] == data2["_id"]


def test_category(seed_data):
    """
    Tests to ensure we retrieve the only fact from the Existentialism category.
    """
    with TestClient(app) as client:
        response = client.get("/phrase/?category=Existentialism")
        assert response.status_code == 200
        data = response.json()
        assert data["phrase"] == "Everybody dies. Live a life you can be proud of."


def test_bad_category(seed_data):
    """
    Tests to ensure the microservice handles requests for nonexistent categories correctly.
    """
    with TestClient(app) as client:
        response = client.get("/phrase/?category=Not_A_Real_Category")
        assert response.status_code == 404
        assert "There are no phrases found for the category:" in response.json()["detail"]


def test_bad_request(seed_data):
    """
    Tests to make sure bad requests are handled correctly
    """
    with TestClient(app) as client:
        response = client.patch("/phrase/?phrase_id=this_is_not_a_valid_mongo_id")
        assert response.status_code == 400
        assert "Invalid ID format" in response.json()["detail"]


@patch('main.collection')
def test_db_error(mock_collection):
    """
    Tests to ensure
    """
    mock_collection.find_one.side_effect = Exception("Database is down!")
    with TestClient(app) as client:
        response = client.get("/phrase/")
        assert response.status_code == 500
