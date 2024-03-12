from os import environ
from json import load
from pymongo import MongoClient

# Helper Method to load database credentials
def load_db_config(file_path: str):
    # Load the file into JSON
    with open(file_path, "r") as buffer:
        # Get the dictionary from JSON File
        vars = load(buffer)
    
    # Update environment variables
    environ.update(vars) 

    # Clear the original vars to not expose in-memory
    vars.clear()

# Method to create Mongo Client
def create_mongo_client(file_path: str) -> MongoClient:
    # Update environment variables
    load_db_config(file_path=file_path)

    # Setup the credentials
    host = environ['MONGO_HOST']
    user = environ['MONGO_USER']
    password = environ['MONGO_PASSWORD']
    port = environ['MONGO_PORT']
    db = environ['MONGO_DB']

    # Connection URI
    uri = f'mongodb://{user}:{password}@{host}:{port}/{db}'

    # Setup the client
    client = MongoClient(uri)

    return client
