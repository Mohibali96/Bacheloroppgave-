import os
import subprocess

# Directory where video files are stored
VIDEO_DIR = 'C:/SoccerNetData'

def convert_videos(video_dir):
    for root, dirs, files in os.walk(video_dir):
        for file in files:
            if file.endswith('.mkv'):
                mkv_path = os.path.join(root, file)
                mp4_path = os.path.splitext(mkv_path)[0] + '.mp4'
                convert_to_mp4(mkv_path, mp4_path)

def convert_to_mp4(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-codec', 'copy',
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Converted {input_path} to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e}")

if __name__ == '__main__':
    convert_videos(VIDEO_DIR)