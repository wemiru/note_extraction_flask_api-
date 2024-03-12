from json import load
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

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

# Create the PostgreSQL engine
def postgres_engine(file_path: str) -> Engine:
    # Get environment variables
    load_db_config(file_path=file_path)

    # Get the details
    host = environ['POSTGRES_HOST']
    user = environ['POSTGRES_USER']
    password = environ['POSTGRES_PASSWORD']
    port = environ['POSTGRES_PORT']
    database = environ['POSTGRES_DATABASE']

    # Create a connection string
    uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'

    # Create the engine
    engine = create_engine(uri)

    return engine
