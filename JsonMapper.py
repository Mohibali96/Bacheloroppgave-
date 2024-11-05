import os
import json

video_base_dir = "C:\\SoccerNetData\\england_epl\\2014-2015"
commentary_base_dir = "C:\\SoccerNetData\\sn-echoes-main\\Dataset\\whisper_v1\\england_epl\\2014-2015"

for match_dir in os.listdir(video_base_dir):
    video_dir = os.path.join(video_base_dir, match_dir)
    commentary_dir = os.path.join(commentary_base_dir, match_dir)
    
    if os.path.isdir(video_dir) and os.path.isdir(commentary_dir):
        match_data = []
        video_files = ["1_720p.mkv", "2_720p.mkv"]
        commentary_files = ["1_asr.json", "2_asr.json"]
        
        for video_file, commentary_file in zip(video_files, commentary_files):
            video_path = os.path.join(video_dir, video_file)
            commentary_path = os.path.join(commentary_dir, commentary_file)
            
            # Load the commentary data with UTF-8 encoding
            with open(commentary_path, "r", encoding="utf-8") as file:
                commentary_data = json.load(file)
            
            # Add to match JSON structure
            match_data.append({
                "video_path": video_path,
                "transcription": commentary_data
            })
        
        # Save the match JSON structure to a new file
        match_json_path = os.path.join(video_dir, "combined_transcriptions.json")
        with open(match_json_path, "w", encoding="utf-8") as json_file:
            json.dump(match_data, json_file, indent=4)

        print(f"Combined data for match saved to {match_json_path}")