from os import environ
from json import load

# Helper Function
def load_env_vars(file_path: str):
    # Create buffer
    with open(file_path, "r") as buffer:
        # Create a dictionary
        vars = load(buffer)
    
    # Update the environment variables
    environ.update(vars) 

    # Clear the variables dictionary
    vars.clear()

