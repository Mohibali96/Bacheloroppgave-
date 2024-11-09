import sqlite3
import json  # For parsing JSON segment data
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
        ['http://localhost:9200'],
        timeout=30,
        max_retries=10,
        retry_on_timeout=True
    )

    # Check if the connection is successful
    if not es.ping():
        raise ValueError("Connection to Elasticsearch failed")

    print("Connection to Elasticsearch successful")

    # Define the index name
    index_name = 'soccernet'

    # Delete the old index if it exists
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Deleted existing index '{index_name}'.")

    # Define the mapping with 'nested' type for transcription.segments
    mapping = {
        "mappings": {
            "properties": {
                "match_dir": {"type": "text"},
                "video_path": {"type": "text"},
                "transcription": {
                    "properties": {
                        "segments": {
                            "type": "nested",  # Specify as nested
                            "properties": {
                                "start_time": {"type": "float"},
                                "end_time": {"type": "float"},
                                "text": {"type": "text"}
                            }
                        }
                    }
                }
            }
        }
    }

    # Create the index with the defined mapping
    es.indices.create(index=index_name, body=mapping)
    print(f"Created index '{index_name}' with nested mapping for segments.")

    # Prepare data for bulk indexing
    actions = []

    for row in rows:
        # Parse the transcription field assuming it's in JSON format
        transcription_data = json.loads(row[3])

        # Extract segments and structure them with start_time, end_time, and text
        segments = [
            {
                "start_time": segment_data[0],
                "end_time": segment_data[1],
                "text": segment_data[2]
            }
            for segment_data in transcription_data["segments"].values()
        ]

        # Add structured document to actions for bulk indexing
        actions.append({
            "_index": index_name,
            "_id": row[0],
            "_source": {
                "match_dir": row[1],
                "video_path": row[2],
                "transcription": {
                    "segments": segments
                }
            }
        })

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
