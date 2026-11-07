import os
from datetime import datetime

import speech_recognition as sr           
from pydub import AudioSegment            
from docx import Document                 
from fpdf import FPDF                     


AudioSegment.converter = "ffmpeg"

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    if audio_file.lower().endswith(".mp3"):
        try:
            wav_path = audio_file[:-4] + ".wav"
            AudioSegment.from_mp3(audio_file).export(wav_path, format="wav")
            audio_file = wav_path
        except Exception as e:
            return f"Error converting MP3 to WAV: {str(e)}"
    try:
        with sr.AudioFile(audio_file) as source:
            print("🔊 Processing audio...")
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Speech recognition service error."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def save_as_word(title, date, day, summary, filepath):
    doc = Document()
    doc.add_heading("Lecture Notes", level=1)
    doc.add_paragraph(f"Title : {title}")
    doc.add_paragraph(f"Date  : {date}")
    doc.add_paragraph(f"Day   : {day}")
    doc.add_heading("Lecture Summary", level=2)
    doc.add_paragraph(summary)
    doc.save(filepath)

def save_as_pdf(title, date, day, summary, filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Lecture Notes", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Title : {title}", ln=True)
    pdf.cell(0, 10, f"Date  : {date}", ln=True)
    pdf.cell(0, 10, f"Day   : {day}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Lecture Summary:", ln=True)
    pdf.set_font("Arial", size=12)
    for line in summary.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filepath)

audio_path = input("📥 Paste the full path to the lecture audio file (mp3): ").strip().strip('"')
if not os.path.isfile(audio_path):
    print("❌ Error: The specified audio file does not exist.")
    exit()

lecture_title = input("📝 Enter the lecture title: ").strip()

save_dir = input("📁 Enter the folder path to save notes: ").strip().strip('"')
if not os.path.isdir(save_dir):
    print("❌ Error: The specified folder does not exist.")
    exit()

file_name = input("💾 Enter the filename (without extension): ").strip()
if not file_name:
    file_name = "Lecture_Notes"


now = datetime.now()
date_today = now.strftime("%Y-%m-%d")
day_today = now.strftime("%A")

lecture_text = speech_to_text(audio_path)

word_path = os.path.join(save_dir, file_name + ".docx")

save_as_word(lecture_title, date_today, day_today, lecture_text, word_path)

print("\n✅ Notes saved successfully!")
print(f"📄 Word file saved at: {word_path}")
