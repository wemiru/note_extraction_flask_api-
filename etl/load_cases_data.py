import pandas as pd
from os import getcwd
from postgres_engine import postgres_engine

# URL to the file
url = "https://ashfaq-nsclc-dataset.s3.amazonaws.com/sukrit_data/multicare_dataset/cases.csv"

# Load into pandas DataFrame
df = pd.read_csv(url)

print("DataFrame read successfully.")

# Configuration to JSON for PostgreSQL
json_path = getcwd() + "/src/projects/project_2/etl/postgres_creds.json"

# Load cursor
cursor = postgres_engine(file_path=json_path).connect()

# Load the cases to a PostgreSQL table
df.to_sql(name='cases', con=cursor, index=False, if_exists='replace')

# Close the connection
cursor.close()

print("Table written successfully!")