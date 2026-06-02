import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Configure Gemini API
GEN_AI_KEY = os.getenv("GEMINI_API_KEY")
if GEN_AI_KEY:
    genai.configure(api_key=GEN_AI_KEY)
else:
    pass

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
        
        # Initialize the API client instance
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch the transcript objects
        transcript = ytt_api.fetch(video_id)
        
        # FIX: Access the '.text' attribute directly instead of using ['text']
        full_text = " ".join([item.text for item in transcript])
        return full_text, None

    except Exception as e:
        return None, f"Error extracting transcript: {str(e)}"

# ----------------------------------------
# Generate AI Summary (Multilingual)
# ----------------------------------------
def generate_summary(transcript_text, target_language):
    try:
        if not GEN_AI_KEY:
            return "Error: Gemini API key not configured. Please set the GEMINI_API_KEY environment variable."

        # FIX: Using the fully qualified production model name 'models/gemini-1.5-flash'
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash"
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
        
        # FIX: Pass generation_config parameters directly into the generate_content call
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.3}
        )
        return response.text

    except Exception as e:
        return f"Error generating summary: {str(e)}"