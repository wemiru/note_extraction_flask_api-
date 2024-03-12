import pandas as pd
from os import getcwd
from sys import path
from sqlalchemy import text
from os.path import dirname, realpath
from flask import request, jsonify

# Import the module from the parent
current = dirname(realpath(__file__))
parent = dirname(current)

# Add the parent path to the system path
path.append(parent)

from __main__ import app
from etl.postgres_engine import postgres_engine

# Setup the engine
json_path = getcwd() + "/etl/postgres_creds.json"

# Global Query Parameters

# Creating routes
@app.route(rule='/case_metadata')
def case_metadata():
    # Query Parameter for number of records
    n_records = request.args.get('n', default=100)
    
    # Setup the cursor
    cursor = postgres_engine(file_path=json_path).connect()

    # Define a PostgreSQL query
    query = f"""
        SELECT *
        FROM cases
        LIMIT {n_records}
    """

    # Get the table
    df = pd.read_sql_query(sql=text(query), con=cursor)

    # Drop the case_text column
    df.drop('case_text', axis=1, inplace=True)

    # Transform the DataFrame into list of objects
    lst_objs = df.to_dict(orient='records')

    # Close db connection
    cursor.close()

    # Return the JSONIFY results
    return jsonify(lst_objs)

# Route for retrieving case_text
@app.route(rule='/case_text')
def case_text():
    # Query Parameter for number of records
    n_records = request.args.get('n', default=100)

    # Setup the cursor
    cursor = postgres_engine(file_path=json_path).connect()

    # Define a PostgreSQL query 
    query = f"""
        SELECT case_id, case_text
        FROM cases
        LIMIT {n_records}
    """

    # Get the table
    df = pd.read_sql_query(sql=text(query), con=cursor)

    # Transform the DataFrame into list of objects
    lst_objs = df.to_dict(orient='records')

    # close connection
    cursor.close()

    return jsonify(lst_objs)
    
