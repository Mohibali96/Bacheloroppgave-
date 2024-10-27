from elasticsearch import Elasticsearch, ConnectionError

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Define the index name
index_name = 'soccernet'

# Define the search term
search_term = "Goalkeeper"

try:
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

    print(f"The term '{search_term}' occurred {total_count} times in the transcriptions.")

except ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

print("Search completed.")