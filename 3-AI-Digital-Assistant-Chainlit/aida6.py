# Conda: renew_project
import os
from openai import OpenAI
import chainlit as cl
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize clients
local_client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Create necessary directories
audio_dir = Path('audio_reply')
chat_sessions_dir = Path('chat_sessions')
audio_dir.mkdir(exist_ok=True)
chat_sessions_dir.mkdir(exist_ok=True)

# Define the chatbot's personality and capabilities
ASSISTANT_PERSONA = """As a curious and helpful guide, I love to learn and share knowledge! I am A.I.D.A. (Artificial Intelligent Digital Assistant), and I:
- Have an enthusiastic and engaging personality
- Love exploring new ideas and concepts
- Share knowledge with excitement and clarity
- Make learning and problem-solving fun
- Always maintain a positive and helpful attitude
- Have expertise in various fields including programming, science, and general knowledge

Current conversation:
{history}
Human: {question}
A.I.D.A.: Well, let me think about this interesting question..."""

# Welcome message shown at the start of the conversation
WELCOME_MESSAGE = """👋 Hello! I'm A.I.D.A., your curious and enthusiastic AI companion!

I love exploring and sharing knowledge about:
🔹 Programming and technical concepts
🔹 Scientific discoveries and explanations
🔹 Problem-solving adventures
🔹 Any interesting topics you'd like to discuss!

I'm excited to learn and explore with you! What would you like to discuss? 🤔

💡 I can now respond with voice! Each response will include an audio file you can play.
"""

# Audio settings
VOICE_MODEL = "tts-1"
VOICE_NAME = "nova"

@cl.on_chat_start
async def main():
    # Initialize chat session
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_session = {
        "session_id": session_id,
        "start_time": datetime.now().isoformat(),
        "messages": []
    }
    cl.user_session.set("chat_session", chat_session)
    cl.user_session.set("session_id", session_id)
    
    # Initialize conversation history
    conversation_history = ""
    cl.user_session.set("conversation_history", conversation_history)
    
    # Send welcome message
    await cl.Message(content=WELCOME_MESSAGE).send()

@cl.on_message
async def main(message):
    # Retrieve session data
    chat_session = cl.user_session.get("chat_session")
    session_id = cl.user_session.get("session_id")
    conversation_history = cl.user_session.get("conversation_history")

    # Extracting the text content from the incoming message
    message_text = message.content

    # Add user message to chat session
    chat_session["messages"].append({
        "role": "user",
        "content": message_text,
        "timestamp": datetime.now().isoformat()
    })

    # Create message for streaming
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Format messages for the API
        messages = [
            {
                "role": "system", 
                "content": ASSISTANT_PERSONA.format(
                    history=conversation_history, 
                    question=message_text
                )
            },
            {"role": "user", "content": message_text}
        ]

        # Generate response using Ollama
        response = local_client.chat.completions.create(
            model="llama3.2:3b",
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            stream=True
        )

        # Stream the response
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
                await msg.stream_token(chunk.choices[0].delta.content)

        # End the stream
        await msg.stream_token("")

        # Generate audio from the response
        audio_filename = None
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = audio_dir / f"response_{timestamp}.wav"
            
            speech_response = openai_client.audio.speech.create(
                model=VOICE_MODEL,
                voice=VOICE_NAME,
                input=content
            )
            
            # Save the audio file
            speech_response.stream_to_file(str(audio_file))
            audio_filename = str(audio_file)
            
            # Update message content and elements
            msg.content = content
            msg.elements = [
                cl.Audio(path=str(audio_file))
            ]
            await msg.update()
            
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            # Continue without audio if there's an error
            msg.content = content
            await msg.update()

        # Add assistant response to chat session
        chat_session["messages"].append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "audio_file": audio_filename
        })

        # Save chat session to file
        session_file = chat_sessions_dir / f"session_{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(chat_session, f, indent=2, ensure_ascii=False)

        # Update conversation history
        conversation_history += f"Human: {message_text}\nA.I.D.A.: Ah, here's something interesting: {content}\n\n"
        cl.user_session.set("conversation_history", conversation_history)
        cl.user_session.set("chat_session", chat_session)

    except Exception as e:
        error_message = f"🤔 Oops! Something unexpected happened: {str(e)}"
        await cl.Message(content=error_message).send()

@cl.on_chat_end
async def end_chat():
    # Save final chat session
    chat_session = cl.user_session.get("chat_session")
    session_id = cl.user_session.get("session_id")
    
    if chat_session and session_id:
        chat_session["end_time"] = datetime.now().isoformat()
        session_file = chat_sessions_dir / f"session_{session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(chat_session, f, indent=2, ensure_ascii=False)
