# Conda: renew_project
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
import json
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI clients
local_client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Chat settings
model = "llama3.2:3b"
temperature = 0.7
max_tokens = 300
voice = "nova"

# Create necessary directories
audio_dir = Path('audio_reply')
chat_sessions_dir = Path('chat_sessions')
audio_dir.mkdir(exist_ok=True)
chat_sessions_dir.mkdir(exist_ok=True)

# Define the assistant's persona
assistant_persona = """You are a highly capable and dedicated AI assistant. You:
- Provide expert guidance and solutions
- Maintain a professional and respectful demeanor
- Focus on delivering accurate and helpful responses
- Serve as a knowledgeable companion to your user
- Communicate clearly and effectively
- Adapt to the user's needs and preferences
"""

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        messages = data.get('messages', [])
        voice_enabled = data.get('voice_enabled', True)
        
        # Always include the system message first
        if not any(msg.get('role') == 'system' for msg in messages):
            messages.insert(0, {"role": "system", "content": assistant_persona})

        # Get response from local LLM
        response = local_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        assistant_response = response.choices[0].message.content

        # Generate speech if voice is enabled
        audio_path = None
        if voice_enabled:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_file = audio_dir / f"response_{timestamp}.wav"
                
                speech_response = openai_client.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=assistant_response
                )
                
                # Save the audio file
                speech_response.stream_to_file(str(audio_file))
                audio_path = str(audio_file)
            except Exception as e:
                print(f"Error generating speech: {str(e)}")

        return jsonify({
            'response': assistant_response,
            'audio_path': audio_path,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/audio_reply/<path:filename>')
def serve_audio(filename):
    return send_from_directory('audio_reply', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
