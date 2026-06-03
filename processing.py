import re
import os
import json
import requests
import json
import requests
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# RAG & Vector DB Imports (Moved cleanly to the top)
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

# Initialize an In-Memory Chroma Client globally
chroma_client = chromadb.Client()

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
# Build a requests.Session loaded with cookies.txt (Netscape format)
# ----------------------------------------
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

# ----------------------------------------
# Get Transcript
# ----------------------------------------
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

# ----------------------------------------
# Generate AI Summary (Multilingual) via Groq
# ----------------------------------------
def generate_summary(collection, target_language):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return "Error: Groq API key not configured."
            return "Error: Groq API key not configured."

        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        # 1. NEW RAG STEP: Pull only the most relevant, dense summary information from the vector DB
        context = retrieve_context(
            collection, 
            query="Provide a comprehensive timeline overview, logical progression of topics, structural main points, and core lessons of this video conversation.", 
            num_results=6  # Grabs the top 6 most informative chunks (~1200-1500 words maximum)
        )

        prompt = f"""
        You are an expert language learning assistant. Analyze the provided context excerpts from a video transcript and generate a comprehensive, structured learning summary.
        
        CRITICAL REQUIREMENT: Write the entire response, including headings, in the target language: {target_language}.
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
        
        Retrieved Transcript Context:
        {context}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert multilingual language learning assistant."},
                {"role": "user", "content": prompt}
                {"role": "system", "content": "You are an expert multilingual language learning assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# ----------------------------------------
# Generate Quiz via Groq
# ----------------------------------------
def generate_quiz(collection, target_language):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return None

        client = OpenAI(
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        # 1. Pull targeted contextual answers by searching the vector DB semantically
        context = retrieve_context(collection, query="What are the main topics, lessons, definitions, and key points explained in this video?", num_results=5)

        prompt = f"""
        You are an expert language teacher. Based strictly on the provided Context excerpts extracted from a video transcript, generate a 5-question multiple-choice quiz to test user understanding.
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

        Retrieved Context Excerpts:
        {context}
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
# ----------------------------------------
# RAG Operations: Vector Storage Initialization
# ----------------------------------------
def create_vector_store(transcript_text, video_id):
    """
    Splits the raw transcript into semantic chunks and stores them in a local vector collection.
    """
    try:
        # Step A: Chunk the transcript text so chunks fit comfortably in embedding windows
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Characters per chunk (~200 words)
            chunk_overlap=200 # Overlap to prevent splitting context mid-sentence
        )
        chunks = text_splitter.split_text(transcript_text)
        
        # Step B: Set up OpenAI embedding function (Requires OPENAI_API_KEY in your .env)
        openai_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Step C: Format unique collection name (Chroma collections can't have hyphens)
        collection_name = f"video_{video_id.replace('-', '_')}"
        
        # Delete old collection if it exists to maintain a fresh processing memory
        try:
            chroma_client.delete_collection(name=collection_name)
        except Exception:
            pass
            
        collection = chroma_client.create_collection(
            name=collection_name, 
            embedding_function=openai_ef
        )
        
        # Step D: Bulk insert chunks into the vector database
        documents = chunks
        ids = [f"id_{idx}" for idx in range(len(chunks))]
        metadatas = [{"source": video_id} for _ in range(len(chunks))]
        
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        return collection, None
    except Exception as e:
        return None, f"Vector storage initialization failed: {str(e)}"

# ----------------------------------------
# RAG Operations: Semantic Retrieval
# ----------------------------------------
def retrieve_context(collection, query, num_results=4):
    """
    Queries the vector database using semantic search and returns the top-K relevant text blocks.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=num_results
        )
        # Flatten retrieved document arrays into a singular context block
        retrieved_documents = results['documents'][0]
        context = "\n\n--- Context Block ---\n\n".join(retrieved_documents)
        return context
    except Exception as e:
        print(f"Retrieval error: {e}")
        return ""