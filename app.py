import streamlit as st

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

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown("""
        <div class="card">
        <h3>📄 AI Summary</h3>
        <p>
        This is where your Gemini/LangChain generated summary
        will appear after processing the transcript.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        <h3>📚 Important Vocabulary</h3>
        </div>
        """, unsafe_allow_html=True)

        vocab_data = {
            "Word": [
                "Transcript",
                "Artificial Intelligence",
                "Vocabulary",
                "Language",
                "Comprehension"
            ],
            "Meaning": [
                "Written version of speech",
                "Machines simulating intelligence",
                "Collection of words",
                "Method of communication",
                "Understanding something"
            ]
        }

        st.table(vocab_data)

    with col2:

        st.markdown("""
        <div class="card">
        <h3>📊 Learning Stats</h3>
        <p>Words Learned: 5</p>
        <p>Quiz Score: 0/3</p>
        <p>Language: Selected Language</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>📝 Vocabulary Quiz</h3>
    </div>
    """, unsafe_allow_html=True)

    q1 = st.radio(
        "1. What is a transcript?",
        [
            "A written version of speech",
            "A video format",
            "A language",
            "An AI model"
        ]
    )

    q2 = st.radio(
        "2. Vocabulary means:",
        [
            "Collection of words",
            "Video subtitles",
            "A language translator",
            "Speech recognition"
        ]
    )

    q3 = st.radio(
        "3. Comprehension means:",
        [
            "Understanding",
            "Translation",
            "Speaking",
            "Reading speed"
        ]
    )

    if st.button("Submit Quiz"):

        score = 0

        if q1 == "A written version of speech":
            score += 1

        if q2 == "Collection of words":
            score += 1

        if q3 == "Understanding":
            score += 1

        st.success(f"🎉 Your Score: {score}/3")

st.markdown("---")
st.caption(
    "Velora-AI | Built with Streamlit, Gemini API, LangChain & LlamaIndex"
)
