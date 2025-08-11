from flask import Flask, request
import os
from transcriber import transcribe_audio
from smart_nlp_pipeline import process_transcript
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# === CONFIGURATION ===

STUDENT_EMAIL = "sreejanjalgam36388@gmail.com"
STUDENT_EMAIL = "pranavadithya1188@gmail.com"
STUDENT_EMAIL = "supratheek2k6@gmail.com"
STUDENT_EMAIL = "sreejan.official.18@gmail.com"
STUDENT_EMAIL = "pranavadithya1234@gmail.com"
STUDENT_EMAIL = "supratheek2k6@gmail.com"
SENDER_EMAIL = "smartscribekmit@gmail.com"            # ✅ Now the sender
SENDER_PASSWORD = "fbzbqggddnesgcva"
def send_pdf_email(pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "📚 Smart Notes Summary"
    msg["From"] = SENDER_EMAIL
    msg["To"] = STUDENT_EMAIL
    msg.set_content("Hi,\n\nPlease find your summarized lecture notes attached as a PDF.\n\nBest regards,\nSmart Notes AI")

    with open(pdf_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="summary_notes.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)

    print(f"📧 Email with PDF sent to {STUDENT_EMAIL}")

@app.route("/upload", methods=["POST"])
def upload_audio():
    audio = request.files.get("audio")
    if not audio:
        return "No audio file provided", 400

    os.makedirs("uploads", exist_ok=True)
    audio_path = os.path.join("uploads", audio.filename)
    audio.save(audio_path)

    print("🧠 Transcribing...")
    transcript = transcribe_audio(audio_path)

    print("🧹 Cleaning and summarizing...")
    process_transcript(transcript, audio_path=audio_path)  # ⬅️ generates PDF and deletes .wav

    print("📤 Sending email...")
    send_pdf_email("summary_notes.pdf")

    return "✅ PDF summary emailed to student", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
