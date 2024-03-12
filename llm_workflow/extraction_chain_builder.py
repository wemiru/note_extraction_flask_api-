import pandas as pd
from sys import path
from functools import reduce
from os import getcwd, environ
from os.path import dirname, realpath
from sqlalchemy import text
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain_pydantic
from ExtractionModel import Properties
from api_key_loader import load_env_vars

# Add a line formatter
def line_formatter():
    print('-'*100)

# Make adjustments to the system path
current = dirname(realpath(__file__))
parent = dirname(current)
path.append(parent) 

# Importing PostgreSQL helper
from etl.postgres_engine import postgres_engine
from etl.mongo_engine import create_mongo_client

# Path to OpenAI API Key
api_key_path = getcwd() + "/llm_workflow/openai_api_key.json"

# Path to the PostgreSQL credentials
postgres_path = getcwd() + "/etl/postgres_creds.json"

# MongoDB Path
mongo_path = getcwd() + "/etl/mongo_creds.json"

# Update environment variables
load_env_vars(file_path=api_key_path)

# Get the connection to PostgreSQL
cursor = postgres_engine(file_path=postgres_path).connect()

# Setup the model
llm = ChatOpenAI(api_key=environ['OPENAI_API_KEY'])

# Setup the chain
chain = create_extraction_chain_pydantic(pydantic_schema=Properties, llm=llm)

# Query
query = """
    SELECT *
    FROM cases
    LIMIT 100
"""

# Read the case_txt from cases table
df = pd.read_sql_query(sql=text(query), con=cursor)

print("cases table from PostgreSQL read successfully.")

line_formatter()

# Cases
ids = df['case_id'].tolist()
txt = df['case_text'].tolist()

# Save results as a dictionary
results = {}

# Create a counter
counter = 0

# Iterate through results
for i in range(len(ids)):
    # Get case_id
    case_id = ids[i]
   
    # corresponding txt
    case_txt = txt[i]

    # Run the chain
    result = chain.run(case_txt)

    # Update the counter
    counter += 1

    print(f"{case_id} text NER completed.")

    # Add the result to the results dictionary
    results[case_id] = result

    print(f"{100 - counter} results remaining.")

line_formatter()

print("Results added successfully!")

line_formatter()

# Setup Mongo Connection
mongo_client = create_mongo_client(file_path=mongo_path)

# Access a database called multicare_ner and a collection called sample_extraction_results
db = mongo_client['multicare_ner']
mongo_collection = db['sample_extraction_results']

print("MongoDB connection successful.")
line_formatter()

# Load the results into the collection
mongo_collection.insert_one(document=results)

print("Results saved to MongoDB collection successfully.")

