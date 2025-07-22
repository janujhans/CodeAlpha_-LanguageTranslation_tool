# app.py

import streamlit as st
import requests
import base64

# Set page config
st.set_page_config(page_title="Language Translator", page_icon="🌍", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        font-size: 3rem;
        font-weight: 450;
        font-family: "Lucida Console", "Courier New", monospace;
        color: #e1e9ed;
        text-shadow: 2px 6px 14px #b0b3b5;
}
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #ecf0f1;
        border-radius: 10px;
        padding: 1rem;
        font-size: 1.1rem;
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: yellow;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title"> Multi-language Translator</div>', unsafe_allow_html=True)

# Sidebar for model selection (optional)
with st.sidebar:
    st.header("⚙️ Settings")
    #model selection
    model_name = st.selectbox("Select LLM Model", ["mistral", "llama2", "gemma"], index=0)
    st.markdown("Make sure this model is available in your Ollama setup.")

  # Language options
    language_options = {
    "Arabic 🇸🇦": "Arabic",
    "Bengali 🇧🇩": "Bengali",
    "Chinese 🇨🇳": "Chinese",
    "Dutch 🇳🇱": "Dutch",
    "English 🇬🇧": "English",
    "French 🇫🇷": "French",    
    "German 🇩🇪": "German",  
    "Hindi 🇮🇳": "Hindi",
    "Italian 🇮🇹": "Italian",
    "Japanese 🇯🇵": "Japanese",
    "Korean 🇰🇷": "Korean",
    "Portuguese 🇵🇹": "Portuguese",
    "Russian 🇷🇺": "Russian",
    "Spanish 🇪🇸": "Spanish",
    "Tamil 🇮🇳": "Tamil",
    "Telugu 🇮🇳": "Telugu",
    "Turkish 🇹🇷": "Turkish",
    "Urdu 🇵🇰": "Urdu"
}

    source_display = st.selectbox("From Language", list(language_options.keys()), index=0)
    target_display = st.selectbox("Target Language", list(language_options.keys()))
    source_language = language_options[source_display]
    target_language = language_options[target_display]
    if source_language == target_language:
        st.warning("⚠️ Source and target languages are the same.")

# Input text area
st.subheader("Enter the text to translate: ")
text_to_translate = st.text_area("✏️ Enter Your text:", height=150, placeholder="Type your text here... ")

# Translate button
if st.button("🌐 Translate"):
    if not text_to_translate:
        st.warning("Please enter some text to translate.")
    elif source_language == target_language:
        st.warning("Please select different source and target languages.")
    else:
        with st.spinner("Translating..."):
            prompt = (
    f"You are a translator. Translate the following text *only* from {source_language} to {target_language}. "
    f"Do not include any extra information or examples. "
    f"Just return the translated sentence.\n\n"
    f"Text: {text_to_translate.strip()}"
)

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }

        try:
                response = requests.post("http://localhost:11434/api/generate", json=payload)
                response.raise_for_status()
                result = response.json()["response"].strip()

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader(f"📘 Translated Text ({target_language})")
                st.write(result)
                st.markdown('</div>', unsafe_allow_html=True)
        except requests.exceptions.RequestException as e:
                st.error(f"❌ Error communicating with Ollama: {e}")
