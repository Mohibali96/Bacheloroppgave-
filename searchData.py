import time
import psutil
from elasticsearch import Elasticsearch, ConnectionError

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Define the index name and search term
index_name = 'soccernet'
search_term = " player"
query_type = "match_phrase"  # Options: "match_phrase", "fuzzy", "multi_match"
multi_match_type = "best_fields"  # Options: "best_fields", "most_fields", "cross_fields", "phrase", "phrase_prefix"

try:
    # Record the start time and initial memory usage
    start_time = time.time()
    process = psutil.Process()
    start_memory = process.memory_info().rss  # Memory in bytes

    # Define the search query based on the query type
    if query_type == "match_phrase":
        query_body = {
            "query": {
                "nested": {
                    "path": "transcription.segments",
                    "query": {
                        "match_phrase": {
                            "transcription.segments.text": search_term
                        }
                    }
                }
            },
            "size": 5  # Limit results to 5
        }
    elif query_type == "fuzzy":
        query_body = {
            "query": {
                "nested": {
                    "path": "transcription.segments",
                    "query": {
                        "fuzzy": {
                            "transcription.segments.text": {
                                "value": search_term,
                                "fuzziness": "AUTO"
                            }
                        }
                    }
                }
            },
            "size": 5  # Limit results to 5
        }
    elif query_type == "multi_match":
        query_body = {
            "query": {
                "nested": {
                    "path": "transcription.segments",
                    "query": {
                        "multi_match": {
                            "query": search_term,
                            "fields": ["transcription.segments.text"],
                            "type": multi_match_type
                        }
                    }
                }
            },
            "size": 5  # Limit results to 5
        }
    else:
        raise ValueError("Invalid query type specified")

    # Perform the search query to get relevant documents
    response = es.search(index=index_name, body=query_body)

    # Initialize a list to store timestamps and video paths
    timestamps = []
    max_timestamps = 5  # Maximum number of timestamps to return
    timestamp_count = 0  # Counter for the number of timestamps collected

    # Iterate through the hits to collect video paths and timestamps from matching segments
    for hit in response['hits']['hits']:
        if timestamp_count >= max_timestamps:
            break  # Stop processing if the maximum number of timestamps is reached

        # Extract video path and segments
        video_path = hit['_source'].get('video_path', 'Unknown Path')  # Default to 'Unknown Path' if not present
        segments = hit['_source']['transcription']['segments']
        
        # Check if video_path exists and has segments
        if video_path and segments:
            # Print the video path
            print(f"Video Path: {video_path}")

            # Iterate through each segment to get the start and end times
            for segment in segments:
                if timestamp_count >= max_timestamps:
                    break  # Stop processing if the maximum number of timestamps is reached

                start_time_value = segment.get("start_time")
                end_time_value = segment.get("end_time")
                text = segment.get("text", "")
                
                # Check if the search term is present in the segment text
                if search_term.lower() in text.lower():
                    # Ensure start_time and end_time are valid before appending
                    if start_time_value is not None and end_time_value is not None:
                        timestamps.append((start_time_value, end_time_value))  # Add start and end time as timestamp
                        timestamp_count += 1  # Increment the counter

            # After listing all timestamps for this video, print them
            if timestamps:
                print(f"The term '{search_term}' was mentioned at the following timestamps (start_time - end_time):")
                for start, end in timestamps:
                    print(f"{start:.2f} - {end:.2f} seconds")
            else:
                print(f"No mentions of '{search_term}' found in this video.")

            # Reset timestamps for next document
            timestamps = []

    # Record end time and memory usage
    end_time = time.time()
    end_memory = process.memory_info().rss

    # Calculate elapsed time and memory usage
    elapsed_time = end_time - start_time
    memory_used = (end_memory - start_memory) / (1024 * 1024)  # Convert bytes to MB

    print(f"Search completed in {elapsed_time:.2f} seconds.")
    print(f"Memory used: {memory_used:.2f} MB")

except ConnectionError as e:
    print(f"Error connecting to Elasticsearch: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

print("Search completed.")