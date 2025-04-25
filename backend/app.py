from flask import Flask, render_template, request, jsonify
import requests
from transformers import pipeline
import os

app = Flask(__name__)

# Summarizer pipeline using HuggingFace model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Deepgram API config
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "your-deepgram-api-key")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"

# Home route for frontend
@app.route('/')
def home():
    return render_template('index.html')  # Now serving index.html from templates folder

@app.route('/summarize', methods=['POST'])
def summarize():
    audio = request.files['audio']
    audio_bytes = audio.read()

    # Step 1: Transcribe with Deepgram
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/webm"
    }
    response = requests.post(DEEPGRAM_URL, headers=headers, data=audio_bytes)
    transcript = response.json().get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")

    if not transcript:
        return jsonify({"summary": "Transcription failed."})

    # Step 2: Summarize transcript
    summary = summarizer(transcript, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
