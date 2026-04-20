import streamlit as st
from datetime import datetime
from ollama import Client
from PIL import Image
import whisper
import os
import tempfile

# --- 1. SETTINGS & HARDWARE OPTIMIZATION ---
st.set_page_config(page_title="Nimittam AI", page_icon="⚡", layout="centered")

# Use e2b for instant speed; e4b for slightly more intelligence
MODEL_NAME = "gemma4:e2b" 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

@st.cache_resource
def load_whisper():
    # 'tiny' is 3x faster than 'base' and fits easily in 11GB RAM
    return whisper.load_model("tiny") 

whisper_model = load_whisper()

# --- 2. UI HEADER ---
st.title("Nimittam AI Chatbot")
if st.session_state.processing:
    st.info("⏳ AI is generating an answer... input is locked.")
else:
    st.success(f"🚀 System Ready | Model: {MODEL_NAME}")
st.markdown("---")

# --- 3. SIDEBAR: MULTIMEDIA ---
with st.sidebar:
    st.header("⚙️ Multimedia Input")
    
    # Inputs are disabled while AI is "processing"
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png"], disabled=st.session_state.processing)
    if uploaded_image:
        st.image(uploaded_image, caption="Image selected", use_container_width=True)
    
    uploaded_audio = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"], disabled=st.session_state.processing)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", disabled=st.session_state.processing):
        st.session_state.messages = []
        st.rerun()

# --- 4. AUDIO TRANSCRIPTION HELPER ---
def transcribe_audio(audio_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.getvalue())
        tmp_path = tmp.name
    # language='en' speeds up the process by skipping language detection
    result = whisper_model.transcribe(tmp_path, fp16=False, language='en')
    os.remove(tmp_path)
    return result["text"]

# --- 5. CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. CHAT LOGIC (THE INPUT LOCK) ---
if prompt := st.chat_input("Type your message...", disabled=st.session_state.processing):
    
    # LOCK THE BUTTON
    st.session_state.processing = True
    
    final_prompt = prompt
    if uploaded_audio:
        with st.status("🎧 Transcribing voice...", expanded=False):
            audio_text = transcribe_audio(uploaded_audio)
            final_prompt = f"{prompt}\n\n[Audio Transcript]: {audio_text}"
    
    # Save User Message
    user_msg = {"role": "user", "content": final_prompt}
    if uploaded_image:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            Image.open(uploaded_image).save(tmp.name)
            user_msg["images"] = [tmp.name]
    
    st.session_state.messages.append(user_msg)
    st.rerun()

# --- 7. AI RESPONSE GENERATION ---
if st.session_state.processing:
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            client = Client(host='http://127.0.0.1:11434')
            
            # TURBO SETTINGS BOKED IN HERE
            response_stream = client.chat(
                model=MODEL_NAME,
                messages=[{"role": m["role"], "content": m["content"], "images": m.get("images", [])} 
                          for m in st.session_state.messages[-4:]], # Only last 4 for speed
                stream=True,
                options={
                    "temperature": 0.1,   # Low temp = Faster, logical answers
                    "num_ctx": 2048,      # Small context = Fast "Thinking" time
                    "num_thread": 8,      # Uses more CPU power
                    "top_k": 40
                },
                keep_alive="60m"          # Model stays in RAM for 1 hour
            )

            for chunk in response_stream:
                token = chunk['message']['content']
                full_response += token
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Hardware Error: {str(e)}")
            full_response = "Connection error. Please check if Ollama is open."

    # UNLOCK THE BUTTON
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.processing = False
    st.rerun()
