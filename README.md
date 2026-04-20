# Nimittam AI Chatbot

## Overview
Nimittam AI is a multimodal chatbot application built with Flet (Flutter for Python). It integrates Ollama for local AI inference with the Gemma 4 model (`gemma4:e4b`), Whisper (`base` model) for potential audio processing, and PIL for image handling. The app features a dark-themed chat UI (450x800 window) with message input, image picker (via file picker), and real-time responses.

## Files
- `app.py`: Main Flet application containing the complete UI and backend logic.

## Requirements
- Python 3.x
- Dependencies (install via pip):
  ```
  pip install flet ollama openai-whisper pillow
  pip install streamlit
  ```

**Setup Ollama:**
1. Download and install from [ollama.com](https://ollama.com)
2. Start the server: `ollama serve`
3. Pull the model: `ollama pull gemma4:e4b`

**Note:** Whisper model (`base`) loads automatically on first use.

## Getting Started
1. Install requirements and set up Ollama (see above).
2. Navigate to the project directory.
3. Run the application:
   ```
   streamlit run app.py
   ```
   This launches a standalone desktop window.

## Usage
- Type messages in the input field (submit with Enter or Send button).
- Attach images using the image icon (supports multimodal queries).
- Bot responses appear in green-bordered containers.
- Supports local processing – no internet required after setup.

## Features
- Image upload support
- Ollama-powered chat
- Auto-scrolling chat history

## Contributing
Feel free to fork, improve, and submit pull requests.

## License
This project is open source and provided as-is.
