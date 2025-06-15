import whisper
import os
from tqdm import tqdm
import pytesseract
from PIL import Image
from llama_index.core.tools import FunctionTool

from ..utils import download_audio_from_youtube, download_video, extract_frames, Logger

LOGGER = Logger.get_logger()


def transcribe_audio(file_path: str, model_size: str = "base") -> str:
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result["text"]


def speech_to_text(video_url: str, model_size: str = "base") -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tmpdir = os.path.abspath(os.path.join(current_dir, "../tmp"))
    os.makedirs(tmpdir, exist_ok=True)
    audio_path = os.path.join(tmpdir, "audio.mp3")
    try:
        LOGGER.info("Downloading audio...")
        download_audio_from_youtube(video_url, audio_path)
        LOGGER.info("Transcribing audio...")
        transcript = transcribe_audio(audio_path, model_size)
        return transcript
    except Exception as e:
        return f"Failed to process video: {e}"


speech_to_text_tool = FunctionTool.from_defaults(
    fn=speech_to_text,
    name="speech_to_text",
    description="Extracts autio from the youtube video and transcribes it to text.",
)


def perform_ocr_on_images(images: list) -> list:
    ocr_results = []
    LOGGER.info("Starting OCR, # of images: %d", len(images))
    for img_path in tqdm(images, desc="Performing OCR", unit="img"):
        text = pytesseract.image_to_string(Image.open(img_path))
        if text:
            LOGGER.info("OCR result for %s: %s", img_path, text.strip())
        ocr_results.append((img_path, text.strip()))
    return ocr_results


def ocr_frame_analysis(
    video_url: str, interval_sec: int = 1, keyword: str = ""
) -> list:
    """Extracts frames from a video and performs OCR on them.
    Args:
        video_url (str): URL of the video to process.
        interval_sec (int): Interval in seconds for frame extraction.
        keyword (str): Keyword to search for in the OCR results.
    Returns:
        list: List of matched text and frame with keyword.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tmpdir = os.path.abspath(os.path.join(current_dir, "../tmp"))
    os.makedirs(tmpdir, exist_ok=True)

    video_path = os.path.join(tmpdir, "video.mp4")
    LOGGER.info("Downloading video...")
    download_video(video_url, video_path)

    LOGGER.info(f"Extracting frames every {interval_sec} seconds...")
    frames = extract_frames(video_path, interval_sec)

    LOGGER.info("Performing OCR with keyword %s", keyword)
    ocr_texts = perform_ocr_on_images(frames)

    keyword_matches = [
        {"frame": os.path.basename(img), "text": text}
        for img, text in ocr_texts
        if keyword.lower() in text.lower()
    ]
    LOGGER.info("Keyword matches %s", keyword_matches)
    return keyword_matches


video_to_text_tool = FunctionTool.from_defaults(
    fn=ocr_frame_analysis,
    name="video_to_text",
    description="Extracts series of frames from the youtube video and performs OCR on them. ",
)
