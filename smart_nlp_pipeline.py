from transformers import pipeline
import re
from spellchecker import SpellChecker
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from datetime import datetime
import os

# === Initialize Models ===
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
spell = SpellChecker()

# === Clean text ===
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'(um+|uh+|like|you know)', '', text, flags=re.IGNORECASE)
    return text.strip()

# === Remove jokes/casual ===
def filter_jokes_and_casual(text):
    lines = text.splitlines()
    casual_keywords = ["joke", "laugh", "funny", "haha", "lol", "bro", "whatever", "anyway"]
    filtered = [line for line in lines if len(line.split()) > 2 and not any(k in line.lower() for k in casual_keywords)]
    return "\n".join(filtered)

# === Spell correct with fallback ===
def correct_spelling(text):
    words = text.split()
    corrected = []
    for w in words:
        if spell.unknown([w]):
            suggestion = spell.correction(w)
            corrected.append(suggestion if suggestion else w)
        else:
            corrected.append(w)
    return " ".join(corrected)

# === Bold keywords in bullet points ===
def bold_keywords(line):
    keywords = ["definition", "importance", "example", "key", "uses", "concept", "application", "result", "theorem", "property", "rule", "method", "formula"]
    for word in keywords:
        line = re.sub(rf'\b({word})\b', r'**\1**', line, flags=re.IGNORECASE)
    return line

# === Convert **text** to <b>text</b> safely ===
def convert_to_html_bold(text):
    parts = text.split("**")
    for i in range(1, len(parts), 2):
        parts[i] = f"<b>{parts[i]}</b>"
    return "".join(parts)

# === Format final summary as bullets ===
def format_bullets(summary_text):
    bullet_lines = summary_text.split(". ")
    formatted = []
    for line in bullet_lines:
        if len(line.strip()) < 5:
            continue
        line = bold_keywords(line.strip())
        formatted.append(f"• {line}.")
    return "\n".join(formatted)

# === Save summary as PDF ===
def save_summary_as_pdf(summary_text, filename="summary_notes.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=LETTER, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=60)
    styles = getSampleStyleSheet()
    bullet_style = ParagraphStyle(
        name='Bullet',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        leftIndent=20,
        spaceAfter=10,
        alignment=TA_LEFT
    )

    header_logo = Image("/Users/sreejanjalagam/Desktop/mac_server/logo.png", width=1.0*inch, height=1.0*inch)
    header_logo.hAlign = 'LEFT'

    title = Paragraph("<b>SmartScribe Summary Notes</b>", styles['Title'])
    subtitle = Paragraph(f"<i>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>", styles['Normal'])
    intro = Paragraph("<b>Overview:</b> This document contains structured highlights automatically generated from lecture audio.", styles['Normal'])
    spacer = Spacer(1, 20)

    content = [header_logo, title, subtitle, spacer, intro, spacer]

    for line in summary_text.split("\n"):
        if line.startswith("•"):
            formatted_line = convert_to_html_bold(line)
            content.append(Paragraph(formatted_line, bullet_style))

    content.append(Spacer(1, 30))

    footer = Paragraph("<font size=10><b>SmartScribe</b> | smartscribekmit@gmail.com | 7013300785</font>", styles['Normal'])
    content.append(footer)

    doc.build(content)
    print(f"✅ PDF saved as: {filename}")

# === Main Function ===
def process_transcript(text, audio_path=None):
    cleaned = clean_text(text)
    filtered = filter_jokes_and_casual(cleaned)
    corrected = correct_spelling(filtered)

    if len(corrected.strip()) == 0:
        return "No valid content to summarize."

    chunks = [corrected[i:i+1024] for i in range(0, len(corrected), 1024)]
    summary = ""

    for chunk in chunks:
        try:
            result = summarizer(chunk, max_length=250, min_length=80, do_sample=False)
            summary += result[0]['summary_text'] + " "
        except Exception:
            summary += "[Error summarizing a section]\n"

    final_output = format_bullets(summary.strip())
    save_summary_as_pdf(final_output)

    # === Delete uploaded audio after processing
    if audio_path and os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"🗑️ Deleted uploaded audio: {audio_path}")

    return final_output