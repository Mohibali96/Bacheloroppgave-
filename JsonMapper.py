import os
import json

video_base_dir = r"C:\SoccerNetData\england_epl\2014-2015"  # Rotmappen for videoene
commentary_base_dir = r"C:\SoccerNetData\england_epl\2014-2015"  # Rotmappen for transkripsjoner

for match_dir in os.listdir(video_base_dir):
    video_dir = os.path.join(video_base_dir, match_dir)
    commentary_dir = os.path.join(commentary_base_dir, match_dir, "dataset")  # Transkripsjoner i "dataset"-mappen

    if os.path.isdir(video_dir) and os.path.isdir(commentary_dir):  # Sjekk at begge mappene eksisterer
        match_data = []  # Holder kampdata
        video_files = [f for f in os.listdir(video_dir) if f.endswith(".mkv")]  # Henter videofiler
        commentary_files = [f for f in os.listdir(commentary_dir) if f.endswith(".json")]  # Henter JSON-filer

        # Matcher videofiler med transkripsjonsfiler (forutsetter likt antall)
        for video_file, commentary_file in zip(video_files, commentary_files):
            video_path = os.path.join(video_dir, video_file)
            commentary_path = os.path.join(commentary_dir, commentary_file)

            # Last inn transkripsjonsdata
            with open(commentary_path, "r", encoding="utf-8") as file:
                commentary_data = json.load(file)

            # Legg til i kampdata
            match_data.append({
                "video_path": video_path,
                "commentary_data": commentary_data
            })

        # Utskrift for verifisering
        print(f"Prosessert {len(match_data)} kamp(er) i {match_dir}")
