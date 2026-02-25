# AI Chatbot

A Streamlit-based AI chatbot application that connects to a local AI model using Ollama.

## Overview

This is a web-based chatbot application built with Streamlit that allows users to interact with a local AI model. The application provides a clean, intuitive chat interface with message history, timestamps, and chat statistics.

## Features

- 💬 **Chat Interface**: Clean and modern chat UI with message bubbles
- 🤖 **Local AI**: Connects to local Ollama AI model (gemma3:4b)
- 📊 **Chat Statistics**: Track total messages and user messages in sidebar
- 🕐 **Timestamps**: View when each message was sent
- 🗑️ **Clear Chat**: Button to reset conversation history
- ⏳ **Thinking Indicator**: Shows spinner while AI is generating response

## Requirements

- Python 3.8+
- Streamlit
- Ollama (running locally)
- 
## Installation

1. Install the required dependencies:

```
bash
pip install streamlit ollama
```

2. Make sure Ollama is installed and running locally with the gemma3:4b model:
   Open Cammand Prompt as Administration and Run This Command One by One 
```
bash
irm https://ollama.com/install.ps1 | iex
ollama serve
ollama pull gemma3:4b
```

## Usage

Run the Streamlit application:

```
bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Configuration

- **Model**: gemma3:4b (configured in the sidebar and code)
- **Ollama Host**: http://127.0.0.1:11434 (default local Ollama port)

## How It Works

1. **Message Input**: Type your message in the chat input box at the bottom
2. **API Call**: The message is sent to the local Ollama API
3. **Response**: The AI generates a response and displays it in the chat
4. **History**: All messages are stored in session state for conversation continuity

## File Structure

```
.
├── app.py          # Main Streamlit application
└── README.md       # This file
```

## Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Web UI framework |
| ollama | Python client for Ollama API |
| datetime | Timestamp handling |

## Troubleshooting

- **Connection Error**: Ensure Ollama is running (`ollama serve`)
- **Model Not Found**: Pull the model first (`ollama pull gemma3:4b`)
- **Port Already in Use**: Check if port 8501 is available for Streamlit

## License

MIT License
