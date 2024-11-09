import os
import json
import re

# Base directories
video_base_dir = "C:\\SoccerNetData\\england_epl\\2014-2015"
commentary_base_dir = "C:\\SoccerNetData\\sn-echoes-main\\Dataset\\whisper_v1\\england_epl\\2014-2015"

# Define keywords to search for in commentary
keywords = ["GoalKeeper", "Goal", "Foul", "Penalty"]

# Function to index keywords within transcription with metadata
def index_keywords(transcription, keywords, match_name, year):
    indexed_data = []
    for segment in transcription.get("segments", []):
        text = segment.get("text", "")
        timestamp = segment.get("start_time")  # Assumes segments have "start_time"
        
        for keyword in keywords:
            if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                indexed_data.append({
                    "match_name": match_name,
                    "year": year,
                    "keyword": keyword,
                    "timestamp": timestamp,
                    "text": text
                })
    return indexed_data

# Process matches for indexing
for match_dir in os.listdir(video_base_dir):
    video_dir = os.path.join(video_base_dir, match_dir)
    commentary_dir = os.path.join(commentary_base_dir, match_dir)
    
    if os.path.isdir(video_dir) and os.path.isdir(commentary_dir):
        match_data = []
        video_files = ["1_720p.mkv", "2_720p.mkv"]
        commentary_files = ["1_asr.json", "2_asr.json"]
        
        # Extract metadata from match directory name (assuming format "matchname_YYYY")
        match_name, year = match_dir.rsplit("_", 1)
        
        # Store all keyword occurrences for the match
        keyword_index = []
        
        for video_file, commentary_file in zip(video_files, commentary_files):
            video_path = os.path.join(video_dir, video_file)
            commentary_path = os.path.join(commentary_dir, commentary_file)
            
            # Load the commentary data
            with open(commentary_path, "r", encoding="utf-8") as file:
                commentary_data = json.load(file)
            
            # Index keywords in transcription
            indexed_keywords = index_keywords(commentary_data, keywords, match_name, year)
            keyword_index.extend(indexed_keywords)
            
            # Add video and transcription data to match structure
            match_data.append({
                "video_path": video_path,
                "transcription": commentary_data
            })
        
        # Save combined transcription and keyword index
        match_json_path = os.path.join(video_dir, "combined_transcriptions.json")
        keyword_index_path = os.path.join(video_dir, "keyword_index.json")
        
        with open(match_json_path, "w", encoding="utf-8") as json_file:
            json.dump(match_data, json_file, indent=4)
        
        with open(keyword_index_path, "w", encoding="utf-8") as json_file:
            json.dump(keyword_index, json_file, indent=4)

        print(f"Combined data for match saved to {match_json_path}")
        print(f"Keyword index for match saved to {keyword_index_path}")
