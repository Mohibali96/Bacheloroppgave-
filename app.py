from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from urllib.parse import unquote
from searchData import search_videos  # Import the updated search function

app = Flask(__name__)

# Directory where video files are stored
VIDEO_DIR = 'C:/SoccerNetData'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_phrase = request.form['search_term']  # Get the phrase from the form

    try:
        # Perform the search query to get relevant documents
        results = search_videos('soccernet', search_phrase)

        # Debugging: Print the number of results
        print(f"Number of results: {len(results)}")
        return render_template('results.html', search_term=search_phrase, results=results)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/video/<path:filename>')
def video(filename):
    # Decode URL-encoded filename
    decoded_filename = unquote(filename)
    filepath = os.path.normpath(os.path.join(VIDEO_DIR, decoded_filename))

    # Check if the file exists
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return jsonify({"error": "File not found"}), 404

    print(f"Serving video from: {filepath}")  # Debugging statement

    # Extract directory and file name
    directory = os.path.dirname(filepath)
    file = os.path.basename(filepath)
    return send_from_directory(directory, file, mimetype='video/mp4')

@app.route('/test_video')
def test_video():
    # Hardcoded test for debugging
    filepath = "C:/SoccerNetData/england_epl/2014-2015/2015-02-21 - 18-00 Chelsea 1 - 1 Burnley.mp4"
    directory = os.path.dirname(filepath)
    file = os.path.basename(filepath)

    if not os.path.isfile(filepath):
        print(f"Test file not found: {filepath}")
        return jsonify({"error": "Test file not found"}), 404

    print(f"Serving test video from: {filepath}")  # Debugging statement
    return send_from_directory(directory, file, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True)
