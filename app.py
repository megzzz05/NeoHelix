import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Placeholder imports for backend functions
from processing import get_transcript, generate_summary

st.set_page_config(
    page_title="Velora-AI | Smart Language Learning",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# Premium Dark Theme & JavaScript Border Glow Styling
# --------------------------------------------------
st.markdown("""
<style>
/* Global App Background Set to Dark Slate */
.stApp {
    background-color: #0B090F;
}

/* Custom Header with Deep Luxury Violet Gradient Background */
.hero-container {
    background: linear-gradient(135deg, #1C162E 0%, #0F0C1B 100%);
    padding: 3rem 2rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 2.5rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.hero-title {
    color: #FFFFFF !important;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: -1px;
}

.hero-subtitle {
    color: #94A3B8 !important;
    font-size: 1.2rem !important;
    font-weight: 400 !important;
}

/* --- THE TRANSLATED REACT BORDERGLOW CARD --- */
.border-glow-card {
    --edge-proximity: 0;
    --cursor-angle: 45deg;
    --edge-sensitivity: 30;
    --color-sensitivity: calc(var(--edge-sensitivity) + 20);
    --border-radius: 28px;
    --glow-padding: 40px;
    --cone-spread: 25;
    --card-bg: #120F17;
    --fill-opacity: 0.5;

    /* Custom variables mimicking your buildGlowVars function */
    --glow-color: hsl(40deg 80% 80% / 100%);
    --glow-color-60: hsl(40deg 80% 80% / 60%);
    --glow-color-50: hsl(40deg 80% 80% / 50%);
    --glow-color-40: hsl(40deg 80% 80% / 40%);
    --glow-color-30: hsl(40deg 80% 80% / 30%);
    --glow-color-20: hsl(40deg 80% 80% / 20%);
    --glow-color-10: hsl(40deg 80% 80% / 10%);

    /* Gradient colors mapping from yours: ['#c084fc', '#f472b6', '#38bdf8'] */
    --gradient-one: radial-gradient(at 80% 55%, #c084fc 0px, transparent 50%);
    --gradient-two: radial-gradient(at 69% 34%, #f472b6 0px, transparent 50%);
    --gradient-three: radial-gradient(at 8% 6%, #38bdf8 0px, transparent 50%);
    --gradient-four: radial-gradient(at 41% 38%, #c084fc 0px, transparent 50%);
    --gradient-five: radial-gradient(at 86% 85%, #f472b6 0px, transparent 50%);
    --gradient-six: radial-gradient(at 82% 18%, #38bdf8 0px, transparent 50%);
    --gradient-seven: radial-gradient(at 51% 4%, #f472b6 0px, transparent 50%);
    --gradient-base: linear-gradient(#c084fc 0 100%);

    position: relative;
    border-radius: var(--border-radius);
    isolation: isolate;
    display: block;
    border: 1px solid rgb(255 255 255 / 15%);
    background: var(--card-bg);
    overflow: visible;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: rgba(0, 0, 0, 0.5) 0px 16px 32px, rgba(0, 0, 0, 0.5) 0px 32px 64px;
}

.border-glow-card::before,
.border-glow-card::after,
.edge-light {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    transition: opacity 0.25s ease-out;
    z-index: -1;
}

/* Interactive Mask Filters matching your exact CSS setup */
.border-glow-card::before {
    border: 1px solid transparent;
    background:
        linear-gradient(var(--card-bg) 0 100%) padding-box,
        linear-gradient(rgb(255 255 255 / 0%) 0% 100%) border-box,
        var(--gradient-one) border-box, var(--gradient-two) border-box, var(--gradient-three) border-box,
        var(--gradient-four) border-box, var(--gradient-five) border-box, var(--gradient-six) border-box,
        var(--gradient-seven) border-box, var(--gradient-base) border-box;

    opacity: calc((var(--edge-proximity) - var(--color-sensitivity)) / (100 - var(--color-sensitivity)));
    
    -webkit-mask-image: conic-gradient(from var(--cursor-angle) at center, black calc(var(--cone-spread) * 1%), transparent calc((var(--cone-spread) + 15) * 1%), transparent calc((100 - var(--cone-spread) - 15) * 1%), black calc((100 - var(--cone-spread)) * 1%));
    mask-image: conic-gradient(from var(--cursor-angle) at center, black calc(var(--cone-spread) * 1%), transparent calc((var(--cone-spread) + 15) * 1%), transparent calc((100 - var(--cone-spread) - 15) * 1%), black calc((100 - var(--cone-spread)) * 1%));
}

.border-glow-card::after {
    border: 1px solid transparent;
    background: var(--gradient-one) padding-box, var(--gradient-two) padding-box, var(--gradient-three) padding-box, var(--gradient-four) padding-box, var(--gradient-five) padding-box, var(--gradient-six) padding-box, var(--gradient-seven) padding-box, var(--gradient-base) padding-box;
    
    -webkit-mask-image: linear-gradient(to bottom, black, black), radial-gradient(ellipse at 50% 50%, black 40%, transparent 65%);
    mask-image: linear-gradient(to bottom, black, black), radial-gradient(ellipse at 50% 50%, black 40%, transparent 65%);
    mask-composite: source-out;
    -webkit-mask-composite: destination-out;
    opacity: calc(var(--fill-opacity) * (var(--edge-proximity) - var(--color-sensitivity)) / (100 - var(--color-sensitivity)));
    mix-blend-mode: soft-light;
}

.edge-light {
    inset: calc(var(--glow-padding) * -1);
    pointer-events: none;
    z-index: -1;
    -webkit-mask-image: conic-gradient(from var(--cursor-angle) at center, black 2.5%, transparent 10%, transparent 90%, black 97.5%);
    mask-image: conic-gradient(from var(--cursor-angle) at center, black 2.5%, transparent 10%, transparent 90%, black 97.5%);
    opacity: calc((var(--edge-proximity) - var(--edge-sensitivity)) / (100 - var(--edge-sensitivity)));
    mix-blend-mode: plus-lighter;
}

.edge-light::before {
    content: "";
    position: absolute;
    inset: var(--glow-padding);
    border-radius: inherit;
    box-shadow:
        inset 0 0 0 1px var(--glow-color), inset 0 0 1px 0 var(--glow-color-60), inset 0 0 3px 0 var(--glow-color-50), inset 0 0 6px 0 var(--glow-color-40), inset 0 0 15px 0 var(--glow-color-30), inset 0 0 25px 2px var(--glow-color-20), inset 0 0 50px 2px var(--glow-color-10),
        0 0 1px 0 var(--glow-color-60), 0 0 3px 0 var(--glow-color-50), 0 0 6px 0 var(--glow-color-40), 0 0 15px 0 var(--glow-color-30), 0 0 25px 2px var(--glow-color-20), 0 0 50px 2px var(--glow-color-10);
}

/* Reset opacity when not interacting */
.border-glow-card:not(:hover)::before,
.border-glow-card:not(:hover)::after,
.border-glow-card:not(:hover) .edge-light {
    opacity: 0 !important;
    transition: opacity 0.6s ease-in-out;
}

/* Custom Text inputs inside Dark Workspace */
label {
    color: #E2E8F0 !important;
    font-weight: 600 !important;
}

div.stTextInput > div > div > input {
    background-color: #1A1625 !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}

/* Premium Tech Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #c084fc 0%, #6C63FF 100%);
    color: white !important;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    border: none;
    font-weight: 700;
    width: 100%;
    box-shadow: 0 4px 20px rgba(192, 132, 252, 0.25);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    box-shadow: 0 6px 24px rgba(192, 132, 252, 0.45);
    transform: translateY(-1px);
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
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const cx = rect.width / 2;
            const cy = rect.height / 2;
            const dx = x - cx;
            const dy = y - cy;
            
            let kx = Infinity;
            let ky = Infinity;
            if (dx !== 0) kx = cx / Math.abs(dx);
            if (dy !== 0) ky = cy / Math.abs(dy);
            const edge = Math.min(Math.max(1 / Math.min(kx, ky), 0), 1);
            
            let degrees = Math.atan2(dy, dx) * (180 / Math.PI) + 90;
            if (degrees < 0) degrees += 360;
            
            card.style.setProperty('--edge-proximity', (edge * 100).toFixed(3));
            card.style.setProperty('--cursor-angle', degrees.toFixed(3) + 'deg');
        });
    });
}
// Continuous polling wrapper to survive Streamlit DOM refreshes
setInterval(initGlow, 1000);
</script>
""", unsafe_allow_html=True)

# --------------------------------------------------
# UI Header
# --------------------------------------------------
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">🌍 Velora-AI</h1>
    <p class="hero-subtitle">Transform any YouTube video into your personal interactive language classroom</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CONFIGURATION HUB (Wrapped inside the BorderGlow Element)
# --------------------------------------------------
st.markdown("""
<div class="border-glow-card">
    <div class="edge-light"></div>
    <h3 style="color: #FFFFFF; margin-top: 0; margin-bottom: 1.5rem; font-weight: 700;">⚡ Configuration Hub</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    youtube_url = st.text_input(
        "🎥 YouTube Video Link",
        placeholder="https://youtube.com/watch?v=... or shorts links",
        key="yt_url_input"
    )

with col2:
    language = st.selectbox(
        "🌐 Target Learning Language",
        ["English", "Hindi", "French", "Spanish", "German", "Malayalam"],
        key="lang_select"
    )

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
generate = st.button("🚀 Begin Smart Extraction")
st.markdown('</div>', unsafe_allow_html=True)  # Closes the border-glow-card wrapper safely

# --------------------------------------------------
# Output Core Processing Logic
# --------------------------------------------------
if generate:
    if not youtube_url:
        st.warning("Please enter a valid YouTube URL first.")
    else:
        if not GROQ_API_KEY:
            st.error("Missing GROQ API Key! Please ensure your local `.env` file has GROQ_API_KEY set.")
        else:
            with st.spinner("Decoding video timestamps and fetching text transcripts..."):
                transcript_text, error = get_transcript(youtube_url)
            
            if error:
                st.error(f"❌ {error}")
            else:
                st.toast("Transcript processed successfully!", icon="✅")
                
                # Dynamic response area using the same design layout blocks
                tab1, tab2 = st.tabs(["✨ Interactive AI Notes", "📄 Raw Video Text"])
                
                with tab1:
                    st.markdown(f"### 🌍 Study Blueprint ({language})")
                    with st.spinner(f"AI is synthesizing deep learning cards..."):
                        summary_result = generate_summary(transcript_text, language)
                    
                    # Wrap output notes cleanly inside a static border glow block variant
                    # Open the HTML wrapper
                    st.markdown(f"""
                    <div class="border-glow-card" style="--edge-proximity: 100; --cursor-angle: 120deg;">
                        <div class="edge-light"></div>
                        <div style="color: #E2E8F0; line-height: 1.7;">
                    """, unsafe_allow_html=True)
                    
                    # Render Markdown safely using Streamlit's native parser inside the container
                    st.markdown(summary_result)
                    
                    # Close the HTML wrapper safely
                    st.markdown("""
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with tab2:
                    st.markdown("### 📋 Captured Raw Output")
                    st.text_area(
                        "Contextual source string:",
                        transcript_text,
                        height=350,
                        disabled=True
                    )
