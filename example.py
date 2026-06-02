import requests

# GET request
response = requests.get("https://cs361-fact-and-phrase-generator.onrender.com/phrase/?category=space")
print(response.json())
print(response.status_code) 

