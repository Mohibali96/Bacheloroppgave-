import os
import json
import whisper
import warnings

# Undertrykk advarsler
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Filbane til rotkatalog for kampene
video_base_dir = r"C:\SoccerNetData\england_epl\2014-2015"

# Whisper-modellen
print("Laster Whisper-modellen...")
model = whisper.load_model("base", device="cpu")
print("Whisper-modellen lastet.")

# Iterer over alle kampmapper i 2014-2015
for match_dir in os.listdir(video_base_dir):
    match_path = os.path.join(video_base_dir, match_dir)
    
    # Sjekk om mappen inneholder kamper
    if not os.path.isdir(match_path):
        print(f"{match_path} er ikke en mappe. Hoppes over.")
        continue

    # Output-katalog for dataset
    output_dir = os.path.join(match_path, "dataset")
    os.makedirs(output_dir, exist_ok=True)

    # Finn alle videofiler i kampmappen
    video_files = [f for f in os.listdir(match_path) if f.endswith((".mkv"))]

    if not video_files:
        print(f"Ingen videofiler funnet i {match_path}. Hoppes over.")
        continue

    print(f"Fant {len(video_files)} videofil(er) i {match_path}: {video_files}")

    # Transkriber hver videofil i kampmappen
    for video_file in video_files:
        video_path = os.path.join(match_path, video_file)
        try:
            print(f"Starter transkripsjon for: {video_file} i {match_path}")
            
            # Transkriber videoen
            result = model.transcribe(video_path, verbose=False, fp16=False)

            # Lagre transkripsjonen som en JSON-fil
            transcription_file = os.path.join(output_dir, f"{os.path.splitext(video_file)[0]}.json")
            with open(transcription_file, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, indent=4)

            print(f"Transkripsjon lagret i: {transcription_file}")

        except Exception as e:
            print(f"Feil under prosessering av {video_file}: {e}")

print("Transkripsjon for alle kampene er fullført!")
