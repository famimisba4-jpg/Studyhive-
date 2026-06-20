"""
StudyHive AI Guider Backend
----------------------------
A simple Flask server that powers the "Ask AI" feature.
Uses Google's Gemini API (free tier, no card needed to start).

Endpoints:
  POST /ask                -> answer a student's question
  POST /summarize          -> summarize uploaded notes into key points
  POST /generate-questions -> create practice questions from a topic/notes

This is built to run for FREE on Render.com or PythonAnywhere
(no local install needed on your end).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # allows your frontend (different domain) to call this backend

# IMPORTANT: never hardcode your real API key here.
# On Render/PythonAnywhere, set this as an Environment Variable named GEMINI_API_KEY
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text


@app.route("/ask", methods=["POST"])
def ask():
    """
    Body: { "question": "...", "grade": "10", "subject": "Biology" }
    """
    data = request.get_json()
    question = data.get("question", "")
    grade = data.get("grade", "10")
    subject = data.get("subject", "")

    prompt = (
        f"You are a friendly tutor helping a grade {grade} student "
        f"with {subject}. Explain clearly and simply, with an example "
        f"if helpful. Question: {question}"
    )

    answer = ask_gemini(prompt)
    return jsonify({"answer": answer})


@app.route("/summarize", methods=["POST"])
def summarize():
    """
    Body: { "notes": "long messy text from uploaded notes" }
    """
    data = request.get_json()
    notes = data.get("notes", "")

    prompt = (
        "Summarize the following study notes into clear, short bullet "
        f"points a student can quickly review:\n\n{notes}"
    )

    summary = ask_gemini(prompt)
    return jsonify({"summary": summary})


@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    """
    Body: { "topic": "Mitosis", "count": 5, "grade": "10" }
    """
    data = request.get_json()
    topic = data.get("topic", "")
    count = data.get("count", 5)
    grade = data.get("grade", "10")

    prompt = (
        f"Create {count} practice questions (with answers) about "
        f"'{topic}' suitable for a grade {grade} student. "
        "Number them clearly."
    )

    questions = ask_gemini(prompt)
    return jsonify({"questions": questions})


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "StudyHive AI Guider backend is running"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
