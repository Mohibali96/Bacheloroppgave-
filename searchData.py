import time
import psutil
from elasticsearch import Elasticsearch, ConnectionError

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Define the index name and search term
index_name = 'soccernet'
search_term = "Chelsea"

try:
    # Record the start time and initial memory usage
    start_time = time.time()
    process = psutil.Process()
    start_memory = process.memory_info().rss  # Memory in bytes

    # Perform the search query to get relevant documents
    response = es.search(
        index=index_name,
        body={
            "query": {
                "nested": {
                    "path": "transcription.segments",
                    "query": {
                        "match": {
                            "transcription.segments.text": search_term
                        }
                    }
                }
            },
            "size": 1000  # Adjust size based on expected results
        }
    )

    # Initialize a list to store timestamps and video paths
    timestamps = []

    # Iterate through the hits to collect video paths and timestamps from matching segments
    for hit in response['hits']['hits']:
        # Extract video path and segments
        video_path = hit['_source'].get('video_path', 'Unknown Path')  # Default to 'Unknown Path' if not present
        segments = hit['_source']['transcription']['segments']
        
        # Check if video_path exists and has segments
        if video_path and segments:
            # Print the video path
            print(f"Video Path: {video_path}")

            # Iterate through each segment to get the start and end times
            for segment in segments:
                start_time_value = segment.get("start_time")
                end_time_value = segment.get("end_time")
                text = segment.get("text", "")
                
                # Check if the search term is present in the segment text
                if search_term.lower() in text.lower():
                    # Ensure start_time and end_time are valid before appending
                    if start_time_value is not None and end_time_value is not None:
                        timestamps.append((start_time_value, end_time_value))  # Add start and end time as timestamp

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
