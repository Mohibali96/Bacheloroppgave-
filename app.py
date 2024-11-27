from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import time
import psutil
from elasticsearch import Elasticsearch, ConnectionError

app = Flask(__name__)

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Directory where video files are stored
VIDEO_DIR = 'C:/SoccerNetData'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    query_type = "match_phrase"  # You can make this dynamic if needed

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
    else:
        return jsonify({"error": "Invalid query type specified"}), 400

    try:
        # Perform the search query to get relevant documents
        response = es.search(index='soccernet', body=query_body)

        results = []
        for hit in response['hits']['hits']:
            video_path = hit['_source'].get('video_path', 'Unknown Path')
            segments = hit['_source']['transcription']['segments']
            timestamps = []

            for segment in segments:
                start_time_value = segment.get("start_time")
                end_time_value = segment.get("end_time")
                text = segment.get("text", "")

                if search_term.lower() in text.lower():
                    if start_time_value is not None and end_time_value is not None:
                        timestamps.append((start_time_value, end_time_value))

            if timestamps:
                results.append({
                    "video_path": video_path.replace('.mkv', '.mp4'),  # Update to use .mp4 files
                    "timestamps": timestamps
                })

            # Limit to 5 results
            if len(results) >= 5:
                break

        print(f"Number of results: {len(results)}")  # Debugging statement
        return render_template('results.html', search_term=search_term, results=results)

    except ConnectionError as e:
        return jsonify({"error": f"Error connecting to Elasticsearch: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/video/<path:filename>')
def video(filename):
    # Ensure the filename is correctly formatted
    filename = filename.replace('%C2%81', '\\').replace('%02', '\\')
    directory = os.path.dirname(filename)
    filename = os.path.basename(filename)
    return send_from_directory(os.path.join(VIDEO_DIR, directory), filename)

if __name__ == '__main__':
    app.run(debug=True)