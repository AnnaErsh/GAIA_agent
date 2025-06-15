import yt_dlp
from yt_dlp import YoutubeDL
import cv2
import tempfile


def download_audio_from_youtube(url: str, output_path: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_video(video_url: str, output_path: str):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_path,
        "quiet": True,
        "merge_output_format": "mp4",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def extract_frames(video_path: str, interval_sec: int = 1) -> list:
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    extracted_images = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % (fps * interval_sec) == 0:
            img_path = tempfile.mktemp(suffix=".jpg")
            cv2.imwrite(img_path, frame)
            extracted_images.append(img_path)
        frame_count += 1

    cap.release()
    return extracted_images
