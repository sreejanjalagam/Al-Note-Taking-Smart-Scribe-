import whisper
import os

def transcribe_audio(audio_path):
    print(f"[INFO] Transcribing: {audio_path}")
    model = whisper.load_model("large")  # 👈 Use tiny for faster speed on Pi/Mac
    result = model.transcribe(audio_path)
    text = result["text"]

    # Save transcript locally
    os.makedirs("transcripts", exist_ok=True)
    out_path = f"transcripts/{os.path.basename(audio_path).replace('.wav', '.txt')}"
    with open(out_path, "w") as f:
        f.write(text)

    print(f"[INFO] Saved transcript: {out_path}")
    return text
