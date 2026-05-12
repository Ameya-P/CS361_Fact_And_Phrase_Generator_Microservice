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
from main import app
from seed_data import seed_data_list

load_dotenv()

def connect_to_test_db():
    MONGO_URI = os.getenv('MONGO_URI')
    client = MongoClient(MONGO_URI)
    db = client["test-microservices"]
    collection = db["test-fact-or-phrase-generator"]
    return collection

@pytest.fixture
def seed_data():
    # setup
    test_collection = connect_to_test_db()
    test_collection.insert_many([document.copy() for document in seed_data_list])
    yield test_collection
    # teardown 
    test_collection.drop()

client = TestClient(app)

# ---- Tests -----

def test_happy_path_no_category(seed_data):
    '''
    Note: call the function twice so we can make sure it returns a different phrase
    Assert status code as well
    '''
    
    pass

def test_happy_path_with_category(seed_data):
    '''
    Note: call the function twice so we can make sure it returns a different phrase
    Assert status code as well
    '''
    pass

def test_bad_request():
    '''
    Assert status code as well
    '''
    pass

@patch('main.collection')
def test_db_error(mock_collection):
    '''
    Assert status code as well
    '''
    mock_collection.find_one.side_effect = Exception("Database is down!")
    with TestClient(app) as client:
        # call the endpoint here
        pass