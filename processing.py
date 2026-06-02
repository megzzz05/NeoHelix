from youtube_transcript_api import YouTubeTranscriptApi
import re

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
            return "Invalid YouTube URL"
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        full_text = " ".join([item.text for item in transcript])

        return full_text

    except Exception as e:
        return f"Error: {str(e)}"
