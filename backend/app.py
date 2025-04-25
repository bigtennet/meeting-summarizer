from flask import Flask, request, jsonify, render_template
import requests
from transformers import pipeline
import os

app = Flask(__name__)

# Summarizer pipeline using HuggingFace model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Deepgram API config
DEEPGRAM_API_KEY = "d2f6d9cbcf1dd7c1d7453a60c1a378d05bcb35df"
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"

@app.route('/')
def home():
    return render_template("summary.html")

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
