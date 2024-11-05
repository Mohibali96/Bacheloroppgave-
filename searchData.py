import time
import psutil
from elasticsearch import Elasticsearch, ConnectionError

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Define the index name and search term
index_name = 'soccernet'
search_term = "Goal"

try:
    # Record the start time and initial memory usage
    start_time = time.time()
    process = psutil.Process()
    start_memory = process.memory_info().rss  # Memory in bytes

    # Perform the search query
    response = es.search(
        index=index_name,
        body={
            "query": {
                "match": {
                    "transcription": search_term
                }
            }
        }
    )

    # Initialize the count
    total_count = 0

    # Iterate through the hits and count occurrences of the search term
    for hit in response['hits']['hits']:
        transcription = hit['_source']['transcription']
        total_count += transcription.lower().count(search_term.lower())

    # Record end time and memory usage
    end_time = time.time()
    end_memory = process.memory_info().rss

    # Calculate elapsed time and memory usage
    elapsed_time = end_time - start_time
    memory_used = (end_memory - start_memory) / (1024 * 1024)  # Convert bytes to MB

    # Display results
    print(f"The term '{search_term}' occurred {total_count} times in the transcriptions.")
    print(f"Search completed in {elapsed_time:.2f} seconds.")
    print(f"Memory used: {memory_used:.2f} MB")

except ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

print("Search completed.")
