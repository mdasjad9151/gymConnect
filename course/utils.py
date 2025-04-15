# transcode.py
import os
import subprocess
from django.conf import settings

def transcode_video(input_path, output_basename):
    resolutions = {
        "144p": "256x144",
        "360p": "640x360",
        "480p": "854x480",
    }
    output_paths = {}

    for label, size in resolutions.items():
        output_path = os.path.join(settings.MEDIA_ROOT, f"transcoded_videos/{label}/{output_basename}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={size}',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-preset', 'ultrafast',
            '-movflags', 'faststart',
            '-y',  # overwrite if exists
            output_path
        ]
        subprocess.run(command)
        output_paths[label] = f"transcoded_videos/{label}/{output_basename}"

    return output_paths
