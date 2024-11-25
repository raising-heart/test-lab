from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import json

app = Flask(__name__)

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

# Define the assistant's persona
assistant_persona = """You are a highly capable and dedicated AI assistant. You:
- Provide expert guidance and solutions
- Maintain a professional and respectful demeanor
- Focus on delivering accurate and helpful responses
- Serve as a knowledgeable companion to your user
"""

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        messages = data.get('messages', [])
        
        # Always include the system message first
        if not any(msg.get('role') == 'system' for msg in messages):
            messages.insert(0, {"role": "system", "content": assistant_persona})

        response = client.chat.completions.create(
            model="llama3.2:3b",  # or your preferred model
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        assistant_response = response.choices[0].message.content
        return jsonify({
            'response': assistant_response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
