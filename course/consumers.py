import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from course.models import CourseVideo
from asgiref.sync import sync_to_async
import asyncio

QUALITY_MAP = {
    '144': '256:-1',
    '240': '426:-1',
    '360': '640:-1',
    '480': '854:-1',
    '720': '1280:-1',
}

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        video_id = query_params.get('id', [None])[0]
        quality = query_params.get('quality', ['360'])[0]
        start = query_params.get('start', ['0'])[0]
        try:
            start = int(float(start))
        except ValueError:
            start = 0

        if quality not in QUALITY_MAP:
            await self.send(text_data='Invalid quality')
            await self.close(code=4002)
            return

        if not video_id:
            await self.close(code=4001)
            return

        try:
            video = await self.get_video_path(video_id)
            input_path = video.video_file.path
            print(f"Input path: {input_path}")
        except CourseVideo.DoesNotExist:
            await self.send(text_data='Video not found.')
            await self.close(code=4004)
            return

        scale = QUALITY_MAP[quality]

        # FFmpeg command
        ffmpeg_cmd = [
    'ffmpeg',
    '-ss', f'{start}',
    '-re',                         # simulate real-time streaming
    '-i', input_path,
    '-vf', f'scale={scale}',        # Adjust video scale (quality)
    '-c:v', 'libx264',              # Video codec
    '-preset', 'veryfast',          # Faster encoding (lower quality vs speed)
    '-tune', 'zerolatency',         # Minimize latency
    '-c:a', 'aac',                  # Audio codec (AAC)
    '-b:a', '128k',                 # Audio bitrate
    '-ar', '44100',                 # Audio sample rate (standard for web)
    '-movflags', 'frag_keyframe+empty_moov+default_base_moof',  # Fragmentation flags for MSE
    '-f', 'mp4',                    # Output format (MP4)
    'pipe:1'                        # Output to stdout (for streaming)
]


        # Run subprocess
        self.ffmpeg_process = await sync_to_async(subprocess.Popen)(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL  # You can change to PIPE for debugging
        )

        await asyncio.sleep(0.5)  # Give ffmpeg time to start
        asyncio.create_task(self.stream_video())

    async def get_video_path(self, video_id):
        return await sync_to_async(CourseVideo.objects.get)(id=video_id)

    async def stream_video(self):
        try:
            # Send header first (initial bytes)
            init_chunk = await asyncio.to_thread(self.ffmpeg_process.stdout.read, 1024*32)
            if init_chunk:
                await self.send(bytes_data=init_chunk)
                # Small delay to ensure the client processes the init segment
                await asyncio.sleep(0.01)
            
            while True:
                # print("loop")
                progress =  16
                chunk = await asyncio.to_thread(self.ffmpeg_process.stdout.read,1024*progress )
                progress =  progress+16
                if progress == 1024:
                    progress = 64
                if not chunk:
                    # print("inside")
                    break
                await self.send(bytes_data=chunk)
                await asyncio.sleep(0.02)  # Small delay to prevent overwhelming client
        except Exception as e:
            print(f"Error streaming video: {e}")
        finally:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'ffmpeg_process'):
            self.ffmpeg_process.terminate()
