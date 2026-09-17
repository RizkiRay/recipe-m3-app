import urllib.request
import os
import subprocess
import whisper

url = "https://www.instagram.com/reel/DdYieOPMrVf/"
req = urllib.request.Request(
    url,
    headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"}
)
res = urllib.request.urlopen(req).read().decode("utf-8")

pos = 0
found = []
while True:
    idx = res.find(".mp4", pos)
    if idx == -1:
        break
    start = res.rfind("https:", max(0, idx - 800), idx)
    end = res.find('"', idx)
    if start != -1 and end != -1:
        clean = res[start:end].replace("\\u0026", "&").replace("\\/", "/")
        if "instagram" in clean or "cdninstagram" in clean or "fbcdn" in clean:
            found.append(clean)
    pos = idx + 4

print(f"Found {len(found)} candidate MP4 streams.")

out_mp3 = "/tmp/alang_tyaz_final.mp3"
if os.path.exists(out_mp3):
    os.remove(out_mp3)

if found:
    stream_url = found[0]
    print("Downloading stream from CDN...")
    cmd = ["ffmpeg", "-y", "-i", stream_url, "-vn", "-acodec", "libmp3lame", out_mp3]
    subprocess.run(cmd, capture_output=True)

if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
    print(f"Audio downloaded ({os.path.getsize(out_mp3)} bytes). Transcribing with Whisper Multilingual...")
    model = whisper.load_model("base")
    tr = model.transcribe(out_mp3, verbose=False)
    print("\n" + "="*50)
    print("CREATOR: @alang_tyaz")
    print("DETECTED LANGUAGE:", tr.get("language"))
    print("WHISPER VOICE TRANSCRIPT:\n")
    print(tr.get("text", "").strip())
    print("="*50 + "\n")
else:
    print("No stream or download failed. Trying yt-dlp with custom headers...")
    cmd_yt = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", out_mp3, url]
    subprocess.run(cmd_yt, capture_output=True)
    if os.path.exists(out_mp3):
        model = whisper.load_model("base")
        tr = model.transcribe(out_mp3, verbose=False)
        print("Whisper Result:\n", tr.get("text", "").strip())
