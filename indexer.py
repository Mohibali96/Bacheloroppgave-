import sqlite3
from elasticsearch import Elasticsearch, helpers, ConnectionError
import requests

# Connect to the SQLite database
conn = sqlite3.connect('soccernet.db')
cursor = conn.cursor()

# Query data from the matches table
cursor.execute('SELECT * FROM matches')
rows = cursor.fetchall()

# Check if Elasticsearch is reachable via HTTP
try:
    response = requests.get('http://localhost:9200')
    if response.status_code == 200:
        print("Elasticsearch is reachable via HTTP")
    else:
        print(f"Unexpected status code: {response.status_code}")
except requests.ConnectionError as e:
    print(f"Error connecting to Elasticsearch via HTTP: {e}")

# Initialize Elasticsearch client with HTTP
try:
    es = Elasticsearch(
        ['http://localhost:9200'],  # Use HTTP
        timeout=30,  # Increase timeout for connection
        max_retries=10,  # Increase the number of retries
        retry_on_timeout=True  # Retry on timeout
    )

    # Check if the connection is successful
    if not es.ping():
        raise ValueError("Connection to Elasticsearch failed")

    print("Connection to Elasticsearch successful")

    # Define the index name
    index_name = 'soccernet'

    # Create the index if it doesn't exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    # Prepare data for bulk indexing
    actions = [
        {
            "_index": index_name,
            "_id": row[0],  # Use the id as the document ID
            "_source": {
                "match_dir": row[1],
                "video_path": row[2],
                "transcription": row[3]
            }
        }
        for row in rows
    ]

    # Bulk index data
    helpers.bulk(es, actions)

    print("Data indexed successfully.")

except ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
except ValueError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection
    conn.close()