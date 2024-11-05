import os
import json
import sqlite3

conn = sqlite3.connect('soccernet.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_dir TEXT,
    video_path TEXT,
    transcription TEXT
)
''')

video_base_dir = "C:\\SoccerNetData\\england_epl\\2014-2015"

for match_dir in os.listdir(video_base_dir):
    match_path = os.path.join(video_base_dir, match_dir)
    if os.path.isdir(match_path):
        json_file_path = os.path.join(match_path, "combined_transcriptions.json")
        
        if os.path.exists(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                match_data = json.load(json_file)
                
                for entry in match_data:
                    cursor.execute('''
                    INSERT INTO matches (match_dir, video_path, transcription)
                    VALUES (?, ?, ?)
                    ''', (match_dir, entry["video_path"], json.dumps(entry["transcription"])))

conn.commit()
conn.close()

print("Database created and data inserted successfully.")