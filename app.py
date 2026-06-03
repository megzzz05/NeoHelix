import streamlit as st
from dotenv import load_dotenv
import os

# Consolidated single clean import interface
from processing import get_transcript, generate_summary, generate_quiz

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Velora-AI | Smart Language Learning",
    page_icon="🌍",
    layout="wide"
)

# Initialize global session variables to prevent dynamic UI rendering exceptions
if "quiz_submitted" not in st.session_state:
    st.session_state["quiz_submitted"] = False
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}

# --- Premium Theme Styles Injector ---
st.markdown("""
<style>
.stApp { background-color: #0B090F; }
.hero-container {
    background: linear-gradient(135deg, #1C162E 0%, #0F0C1B 100%);
    padding: 3rem 2rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 2.5rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}
.hero-title { color: #FFFFFF !important; font-size: 3.2rem !important; font-weight: 800 !important; margin-bottom: 0.5rem !important; }
.hero-subtitle { color: #94A3B8 !important; font-size: 1.2rem !important; }
.border-glow-card {
    position: relative; border-radius: 28px; isolation: isolate; display: block;
    border: 1px solid rgb(255 255 255 / 15%); background: #120F17; padding: 2.5rem; margin-bottom: 2rem;
    box-shadow: rgba(0, 0, 0, 0.5) 0px 16px 32px;
}
.edge-light { position: absolute; inset: -40px; pointer-events: none; z-index: -1; mix-blend-mode: plus-lighter; }
label { color: #E2E8F0 !important; font-weight: 600 !important; }
div.stTextInput > div > div > input { background-color: #1A1625 !important; color: #FFFFFF !important; border-radius: 12px !important; }
.stButton > button {
    background: linear-gradient(135deg, #c084fc 0%, #6C63FF 100%); color: white !important;
    border-radius: 12px; padding: 0.75rem 2rem; border: none; font-weight: 700; width: 100%;
}
</style>
<script>
const parentDoc = window.parent.document;
function initGlow() {
    const cards = parentDoc.querySelectorAll('.border-glow-card');
    cards.forEach(card => {
        if(card.getAttribute('data-glow-attached')) return;
        card.setAttribute('data-glow-attached', 'true');
        card.addEventListener('pointermove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; const y = e.clientY - rect.top;
            const cx = rect.width / 2; const cy = rect.height / 2;
            const dx = x - cx; const dy = y - cy;
            let kx = Infinity, ky = Infinity;
            if (dx !== 0) kx = cx / Math.abs(dx); if (dy !== 0) ky = cy / Math.abs(dy);
            const edge = Math.min(Math.max(1 / Math.min(kx, ky), 0), 1);
            let degrees = Math.atan2(dy, dx) * (180 / Math.PI) + 90;
            if (degrees < 0) degrees += 360;
            card.style.setProperty('--edge-proximity', (edge * 100).toFixed(3));
            card.style.setProperty('--cursor-angle', degrees.toFixed(3) + 'deg');
        });
    });
}
setInterval(initGlow, 1000);
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-container"><h1 class="hero-title">🌍 Velora-AI</h1><p class="hero-subtitle">Transform any YouTube video into your personal interactive language classroom</p></div>', unsafe_allow_html=True)

st.markdown('<div class="border-glow-card"><h3 style="color: #FFFFFF; margin-top: 0; margin-bottom: 1.5rem; font-weight: 700;">⚡ Configuration Hub</h3>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1], gap="medium")
with col1:
    youtube_url = st.text_input("🎥 YouTube Video Link", placeholder="https://youtube.com/watch?v=...", key="yt_url_input")
with col2:
    language = st.selectbox("🌐 Target Learning Language", ["English", "Hindi", "French", "Spanish", "German", "Malayalam"], key="lang_select")

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
generate = st.button("🚀 Begin Smart Extraction")
st.markdown('</div>', unsafe_allow_html=True)

if generate:
    if not youtube_url:
        st.warning("Please enter a valid YouTube URL first.")
    elif not GROQ_API_KEY:
        st.error("Missing GROQ API Key! Check your local environment configurations.")
    else:
        with st.spinner("Decoding video timestamps and fetching text transcripts..."):
            transcript_text, error = get_transcript(youtube_url)

        if error:
            st.error(f"❌ {error}")
        else:
            st.toast("Transcript processed successfully!", icon="✅")
            with st.spinner("AI is synthesizing deep learning cards..."):
                summary_result = generate_summary(transcript_text, language)
            with st.spinner("Generating personalized quiz questions..."):
                quiz_data = generate_quiz(transcript_text, language)

            st.session_state["transcript_text"] = transcript_text
            st.session_state["summary_result"] = summary_result
            st.session_state["quiz_data"] = quiz_data
            st.session_state["current_language"] = language
            st.session_state["quiz_submitted"] = False
            st.session_state["user_answers"] = {}
            st.rerun()

if st.session_state.get("transcript_text"):
    transcript_text = st.session_state["transcript_text"]
    summary_result  = st.session_state["summary_result"]
    language_label  = st.session_state.get("current_language", "English")

    tab1, tab2, tab3 = st.tabs(["✨ Interactive AI Notes", "📄 Raw Video Text", "🧠 Smart MCQ Quiz"])

    with tab1:
        st.markdown(f"### 🌍 Study Blueprint ({language_label})")
        st.markdown('<div class="border-glow-card"><div style="color: #E2E8F0; line-height: 1.7;">', unsafe_allow_html=True)
        st.markdown(summary_result)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📋 Captured Raw Output")
        st.text_area("Contextual source string:", transcript_text, height=350, disabled=True)

    with tab3:
        st.markdown(f"### 🧠 Interactive Language Quiz ({language_label})")
        quiz = st.session_state.get("quiz_data")

        if not quiz:
            st.error("Failed to generate the quiz structure.")
        else:
            st.markdown('<div class="border-glow-card" style="padding: 2rem;">', unsafe_allow_html=True)

            if not st.session_state.get("quiz_submitted"):
                with st.form(key="quiz_form"):
                    current_answers = {}
                    for idx, q in enumerate(quiz):
                        st.markdown(f"#### **Q{idx+1}. {q['question']}**")
                        current_answers[idx] = st.radio(
                            "Choose answer:", options=q['options'], key=f"q_{idx}", index=None, label_visibility="collapsed"
                        )
                        st.markdown("<br>", unsafe_allow_html=True)
                    
                    submit_quiz = st.form_submit_button("📊 Submit My Answers")
                
                if submit_quiz:
                    st.session_state["quiz_submitted"] = True
                    st.session_state["user_answers"] = current_answers
                    st.rerun()

            if st.session_state.get("quiz_submitted"):
                saved_answers = st.session_state["user_answers"]
                score = sum(1 for idx, q in enumerate(quiz) if saved_answers.get(idx) == q["correct_answer"])

                st.markdown(f"### 🎯 Final Score: `{score} / {len(quiz)}`")
                st.progress(score / len(quiz))

                if score == len(quiz):
                    st.balloons()
                    st.success("🎉 Perfect Score!")

                for idx, q in enumerate(quiz):
                    user_ans = saved_answers.get(idx)
                    correct_ans = q["correct_answer"]
                    with st.expander(f"Question {idx+1}: {q['question']}", expanded=True):
                        st.write(f"**Your Choice:** `{user_ans if user_ans else 'Unanswered'}`")
                        st.write(f"**Correct Answer:** `{correct_ans}`")
                        st.markdown("🟩 **Result:** Correct!" if user_ans == correct_ans else "🟥 **Result:** Incorrect.")
                        st.info(f"💡 **Explanation:** {q['explanation']}")

                if st.button("🔄 Retake Quiz"):
                    st.session_state["quiz_submitted"] = False
                    st.session_state["user_answers"] = {}
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)
