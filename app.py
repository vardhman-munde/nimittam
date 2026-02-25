import streamlit as st
from datetime import datetime
from ollama import Client 
import os
st.set_page_config(page_title="AI Chatbot", page_icon="💬", layout="centered")
if "messages" not in st.session_state:
    st.session_state.messages = []
st.title("Nimittam  Chatbot")
st.markdown("---")
with st.sidebar:
    st.header("⚙️ Settings")  
    st.markdown("**Model: gemma3:4b**")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("**Chat Statistics:**")
    st.markdown(f"Total Messages: {len(st.session_state.messages)}")
    user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.markdown(f"User Messages: {user_count}")
def get_ollama_response(model="gemma3:4b"):
    try:
        client = Client(host='http://127.0.0.1:11434') 
        api_messages = []
        for msg in st.session_state.messages:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        response = client.chat(
            model=model,
            messages=api_messages
        )
        return response['message']['content']
    except Exception as e:
        return f"Error connecting to local AI: {str(e)}"
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"🕐 {message['timestamp']}")
if prompt := st.chat_input("Type your message here..."):  
    timestamp = datetime.now().strftime("%H:%M")
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕐 {timestamp}")
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": timestamp
    })
    with st.spinner("🤔 Thinking..."):  
        response = get_ollama_response(model="gemma3:4b")
    timestamp = datetime.now().strftime("%H:%M")   
    with st.chat_message("assistant"):
        st.markdown(response)
        st.caption(f"🕐 {timestamp}")
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": timestamp
    })
