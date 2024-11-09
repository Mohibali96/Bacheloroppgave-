import requests
import os
import sys
import ctypes  # Required to load the DLL
import vlc

# Set the VLC directory (adjust this to the confirmed path)
vlc_path = r'C:\Program Files\VideoLAN\VLC'

# Add VLC path to the system path if not already present
if vlc_path not in sys.path:
    sys.path.append(vlc_path)

# Load the libvlc DLL manually if needed
ctypes.CDLL(os.path.join(vlc_path, 'libvlc.dll'))

# Example of making an HTTP request to Elasticsearch
response = requests.get("http://localhost:9200/soccernet/_search")
print(response.json())

# VLC code to play a video
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new("path/to/your/video.mp4")
player.set_media(media)
player.play()
