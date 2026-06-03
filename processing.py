import re
import os
import json
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

load_dotenv()

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def _build_session_with_cookies(cookie_path):
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    })
    with open(cookie_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, _, path, secure, _, name, value = parts[:7]
            session.cookies.set(name, value, domain=domain.lstrip("."), path=path)
    return session

def get_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            return None, "Invalid YouTube URL"

        cookie_path = "cookies.txt" if os.path.exists("cookies.txt") else None

        try:
            if cookie_path:
                session = _build_session_with_cookies(cookie_path)
                api = YouTubeTranscriptApi(http_client=session)
            else:
                api = YouTubeTranscriptApi()

            transcript = api.fetch(video_id)

        except Exception as inner_e:
            err_str = str(inner_e).lower()
            is_ip_ban = any(k in err_str for k in [
                "blocking", "ipblocked", "requestblocked", "could not retrieve"
            ])
            if is_ip_ban:
                if not cookie_path:
                    return None, "IP_BLOCKED_NO_COOKIES"
                else:
                    return None, "IP_BLOCKED_WITH_COOKIES"
            return None, f"Error extracting transcript: {str(inner_e)}"

        full_text = " ".join([item.text for item in transcript])
        return full_text, None

    except Exception as e:
        return None, f"Error extracting transcript: {str(e)}"

def generate_summary(transcript_text, target_language):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return "Error: Groq API key not configured."

        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        prompt = f"""
        You are an expert language learning assistant. Analyze the following YouTube video transcript and generate a comprehensive, structured learning summary.
        
        CRITICAL REQUIREMENT: Write the entire response, including headings, in the target language: {target_language}.
        
        Provide the output matching this structure exactly:
        
        ### 📌 Core Concept Overview
        [Provide a high-level overview of what the video covers in 3-4 sentences]
        
        ### 🔑 Key Takeaways
        * [Key point 1]
        * [Key point 2]
        * [Key point 3]
        
        ### 📝 Detailed Section Breakdown
        [Provide a detailed narrative summary breaking down the logical sections of the discussion]
        
        Transcript text:
        {transcript_text}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert multilingual language learning assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_quiz(transcript_text, target_language):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return None

        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        # Adjusted system prompt for explicit root dictionary schema compliance
        prompt = f"""
        You are an expert language teacher. Based on the following transcript, generate a 5-question multiple-choice quiz to test user understanding.
        The questions, options, and explanations must be written completely in the target language: {target_language}.
        
        You must return a JSON object with a top-level key "quiz" containing the array of questions.
        
        Expected JSON format:
        {{
          "quiz": [
            {{
              "question": "Question text here?",
              "options": ["Option A", "Option B", "Option C", "Option D"],
              "correct_answer": "The exact string match of the correct option",
              "explanation": "Brief explanation of why this is correct."
            }}
          ]
        }}

        Transcript text:
        {transcript_text}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict JSON object generator for language learning quizzes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )

        raw_content = response.choices[0].message.content
        quiz_data = json.loads(raw_content)

        if isinstance(quiz_data, dict):
            if "quiz" in quiz_data:
                return quiz_data["quiz"]
            if "questions" in quiz_data:
                return quiz_data["questions"]
        return quiz_data

    except Exception as e:
        print(f"Quiz generation error: {e}")
        return None
