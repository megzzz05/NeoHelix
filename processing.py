import re
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# Load .env explicitly here too — ensures key is available
# even when processing.py is imported before app.py calls load_dotenv()
load_dotenv()

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
        full_text = " ".join([item.text for item in transcript])
        return full_text, None

    except Exception as e:
        return None, f"Error extracting transcript: {str(e)}"

# ----------------------------------------
# Generate AI Summary (Multilingual) via Grok
# ----------------------------------------
def generate_summary(transcript_text, target_language):
    try:
        # 1. Switch to the Groq API key variable
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            return "Error: Groq API key not configured. Please set the GROQ_API_KEY environment variable."

        # 2. Point to Groq's OpenAI-compatible base URL
        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        prompt = f"""
        You are an expert language learning assistant. Your task is to analyze the following YouTube video transcript and generate a comprehensive, structured learning summary.
        
        CRITICAL REQUIREMENT: You must write the entire response, including headings, in the target language: {target_language}.
        
        Provide the output matching this structure exactly:
        
        ### 📌 Core Concept Overview
        [Provide a high-level overview of what the video covers in 3-4 sentences]
        
        ### 🔑 Key Takeaways
        * [Key point 1]
        * [Key point 2]
        * [Key point 3]
        ...
        
        ### 📝 Detailed Section Breakdown
        [Provide a detailed narrative summary breaking down the logical sections of the discussion]
        
        Transcript text:
        {transcript_text}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # 3. Swap 'grok-3' for a valid Groq model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert multilingual language learning assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating summary: {str(e)}"