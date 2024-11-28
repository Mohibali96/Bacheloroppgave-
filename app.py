from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from searchData import search_videos  # Import the search function

app = Flask(__name__)

# Directory where video files are stored
VIDEO_DIR = 'C:/SoccerNetData'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    query_type = "fuzzy"  

    try:
        # Perform the search query to get relevant documents
        results = search_videos('soccernet', search_term, query_type)

        print(f"Number of results: {len(results)}")  # Debugging statement
        return render_template('results.html', search_term=search_term, results=results)

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