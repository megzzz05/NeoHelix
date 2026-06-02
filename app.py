import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

from processing import get_transcript

st.set_page_config(
    page_title="Velora-AI",
    page_icon="🌍",
    layout="wide"
)


st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    text-align: center;
    color: #6C63FF;
}

.hero-text {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.stButton > button {
    background-color: #6C63FF;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #574bdb;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("""
<h1>🌍 Velora-AI</h1>
<p class="hero-text">
AI-Powered Language Learning Assistant using YouTube Videos
</p>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🎥 Video Analysis")

youtube_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://youtube.com/watch?v=..."
)

language = st.selectbox(
    "🌐 Select Summary Language",
    [
        "English",
        "Hindi",
        "French",
        "Spanish",
        "German",
        "Malayalam"
    ]
)

generate = st.button("🚀 Generate Learning Content")

st.markdown('</div>', unsafe_allow_html=True)

if generate:
    transcript_text = get_transcript(youtube_url)
    st.write("Transcript Extracted Successfully ✅")
    st.text_area(
        "Extracted Transcript",
        transcript_text,
        height=250
    )
