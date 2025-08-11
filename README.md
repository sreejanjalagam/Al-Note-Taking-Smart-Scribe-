# Al Note Taking (Smart Scribe)
SmartScribe is an AI-driven, fully automated note-taking solution integrating Raspberry Pi and macOS. It captures audio via Bluetooth microphone, transcribes speech, generates concise bullet-point summaries, produces a professionally formatted PDF, and delivers it instantly via email—completely hands-free

## 📌 Features

- **🎤 Automatic Recording** – Starts recording when a Bluetooth microphone is connected; stops when disconnected.  
- **📡 Seamless Upload** – Automatically sends audio to the Mac server via HTTP POST.  
- **📝 AI Transcription** – Converts speech to text with high accuracy.  
- **✍ Intelligent Summarization** – Creates concise, keyword-focused bullet points.  
- **📄 Professional PDF Output** – Includes a custom header, footer, and branding.  
- **📧 Instant Email Delivery** – Sends the generated PDF to your email automatically.  
- **🔄 Hands-Free Operation** – No commands or manual triggers required.  

---

## ⚙ System Architecture

```text
Bluetooth Mic → Raspberry Pi (record + detect mic) → HTTP Upload → macOS Server (Flask)
→ Speech-to-Text → Summarization → PDF Generation → Email Delivery

