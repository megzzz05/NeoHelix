
import re
import os
import json
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------
load_dotenv()


# ----------------------------------------
# Reusable Groq Client
# ----------------------------------------
def get_client():
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise Exception("GROQ_API_KEY missing")

    return OpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )


# ----------------------------------------
# Extract Video ID from YouTube URL
# ----------------------------------------
def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    return None


# ----------------------------------------
# Get Transcript
# ----------------------------------------
def get_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)

        if not video_id:
            return None, "Invalid YouTube URL"

        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)

        full_text = " ".join(
            [item.text for item in transcript]
        )

        return full_text, None

    except Exception as e:
        return None, (
            f"Error extracting transcript: {str(e)}"
        )


# ----------------------------------------
# Generate Summary
# ----------------------------------------
def generate_summary(
    transcript_text,
    target_language
):
    try:
        client = get_client()

        prompt = f"""
You are an expert multilingual language learning assistant.

Your task is to analyze the following YouTube transcript and generate a structured educational summary.

IMPORTANT:
Write the ENTIRE response in:
{target_language}

Use this format exactly:

### 📌 Core Concept Overview
Provide a short overview in 3–4 sentences.

### 🔑 Key Takeaways
- Key point 1
- Key point 2
- Key point 3

### 📝 Detailed Section Breakdown
Provide a detailed explanation of the transcript.

Transcript:
{transcript_text[:12000]}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an expert language learning assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:
        return (
            f"Error generating summary: {str(e)}"
        )


# ----------------------------------------
# Vocabulary Extraction
# ----------------------------------------
def generate_vocabulary(
    transcript_text,
    target_language
):
    try:
        client = get_client()

        prompt = f"""
You are an expert vocabulary extraction assistant.

Extract 15 important vocabulary words from the transcript.

For each word provide:
1. meaning
2. translation in {target_language}
3. example sentence

Return ONLY valid JSON.

Example format:

[
    {{
        "word": "innovation",
        "meaning": "new method or idea",
        "translation": "translated word",
        "example": "Innovation drives progress."
    }}
]

Transcript:
{transcript_text[:12000]}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return json.loads(content)

    except Exception as e:
        return {
            "error":
            f"Vocabulary error: {str(e)}"
        }


# ----------------------------------------
# Keyword Extraction
# ----------------------------------------
def generate_keywords(transcript_text):
    try:
        client = get_client()

        prompt = f"""
Extract the 20 most important keywords
from the transcript.

Return ONLY valid JSON list.

Example:
[
    "AI",
    "Machine Learning",
    "Language Model"
]

Transcript:
{transcript_text[:12000]}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return json.loads(content)

    except Exception:
        return []


# ----------------------------------------
# Generate MCQs
# ----------------------------------------
def generate_mcqs(
    transcript_text,
    target_language
):
    try:
        client = get_client()

        prompt = f"""
Generate 10 high-quality MCQs from the transcript.

Rules:
- medium difficulty
- 4 options
- one correct answer
- avoid ambiguity
- test understanding
- language = {target_language}

Return ONLY valid JSON.

Example:

[
    {{
        "question": "What is AI?",
        "options": [
            "Animal",
            "Artificial Intelligence",
            "Computer",
            "Internet"
        ],
        "answer":
        "Artificial Intelligence"
    }}
]

Transcript:
{transcript_text[:12000]}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return json.loads(content)

    except Exception as e:
        return {
            "error":
            f"MCQ generation error: {str(e)}"
        }


# ----------------------------------------
# Improve MCQ Quality
# ----------------------------------------
def validate_mcqs(mcqs):
    try:
        client = get_client()

        prompt = f"""
You are an MCQ quality reviewer.

Review and improve the following MCQs.

Fix:
- ambiguity
- weak distractors
- poor wording
- clarity
- factual mistakes

Return ONLY improved JSON.

MCQs:
{json.dumps(mcqs)}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return json.loads(content)

    except Exception:
        return mcqs

