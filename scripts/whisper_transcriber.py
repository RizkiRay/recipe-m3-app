import os, sys, json, urllib.request, websockets, asyncio, subprocess
from pathlib import Path
import whisper

# Load lightweight multilingual base model (fast on Mac CPU/MPS)
print("Loading Whisper model (base multilingual)...")
whisper_model = whisper.load_model("base")
print("Whisper model loaded successfully!")

def download_reel_audio(reel_url, output_path="/tmp/reel_audio.mp3"):
    if os.path.exists(output_path):
        os.remove(output_path)
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--output", output_path,
        reel_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(output_path):
        return output_path
    return None

def transcribe_audio(audio_path):
    result = whisper_model.transcribe(audio_path)
    return {
        "text": result.get("text", "").strip(),
        "language": result.get("language", "id"),
        "segments": result.get("segments", [])
    }

if __name__ == "__main__":
    test_url = "https://www.instagram.com/reel/DdGXJI4Bb4n/"
    print(f"Testing audio extraction for: {test_url}")
    audio = download_reel_audio(test_url)
    if audio:
        print("Transcribing with Whisper...")
        trans = transcribe_audio(audio)
        print("Language detected:", trans["language"])
        print("Transcript:\n", trans["text"])
    else:
        print("Failed to download audio directly.")
