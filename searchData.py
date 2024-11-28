import time
import psutil
from elasticsearch import Elasticsearch, ConnectionError

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def search_videos(index_name, search_term, query_type="fuzzy", multi_match_type="best_fields"):
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

        # Initialize a list to store results
        results = []

        # Iterate through the hits to collect video paths and timestamps from matching segments
        for hit in response['hits']['hits']:
            video_path = hit['_source'].get('video_path', 'Unknown Path')  # Default to 'Unknown Path' if not present
            segments = hit['_source']['transcription']['segments']
            timestamps = []

            # Check if video_path exists and has segments
            if video_path and segments:
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

                if timestamps:
                    results.append({
                        "video_path": video_path.replace('.mkv', '.mp4'),  # Update to use .mp4 files
                        "timestamps": timestamps
                    })

        # Record end time and memory usage
        end_time = time.time()
        end_memory = process.memory_info().rss

        # Calculate elapsed time and memory usage
        elapsed_time = end_time - start_time
        memory_used = (end_memory - start_memory) / (1024 * 1024)  # Convert bytes to MB

        print(f"Search completed in {elapsed_time:.2f} seconds.")
        print(f"Memory used: {memory_used:.2f} MB")

        return results

    except ConnectionError as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage (can be removed or commented out when integrating with Flask app)
if __name__ == "__main__":
    index_name = 'soccernet'
    search_term = "the player"
    results = search_videos(index_name, search_term)
    for result in results:
        print(result)