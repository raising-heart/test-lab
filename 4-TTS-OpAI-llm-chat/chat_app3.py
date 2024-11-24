# Conda: renew_project
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Create necessary directories if they don't exist
AUDIO_DIR = Path('audio_reply')
CHAT_HISTORY_DIR = Path('chat_history')
AUDIO_DIR.mkdir(exist_ok=True)
CHAT_HISTORY_DIR.mkdir(exist_ok=True)

def get_llm_response(prompt):
    """Get text response from LLM"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting LLM response: {e}")
        return None

def generate_speech(text):
    """Generate speech from text and save to file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_file = AUDIO_DIR / f"response_{timestamp}.wav"
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        
        # Save the audio file
        response.stream_to_file(str(audio_file))
        return str(audio_file)
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

def save_chat_history(chat_file, role, message, audio_file=None):
    """Save chat message to history file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(chat_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{timestamp}] {role}: {message}")
        if audio_file:
            f.write(f"\n[{timestamp}] Audio saved to: {audio_file}")
        f.write("\n" + "-"*50 + "\n")

def chat():
    """Main chat loop"""
    print("Welcome to the Chat App! (Type 'quit' to exit)")
    print("Using Nova voice for responses")
    print("Chat history will be saved in the chat_history folder")
    print("-" * 50)
    
    # Create a new chat history file for this session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chat_file = CHAT_HISTORY_DIR / f"chat_session_{timestamp}.txt"
    
    # Save initial session info
    with open(chat_file, 'w', encoding='utf-8') as f:
        f.write(f"Chat Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            # Save exit message to chat history
            save_chat_history(chat_file, "System", "Chat session ended")
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        # Save user input to chat history
        save_chat_history(chat_file, "User", user_input)
            
        # Get text response
        text_response = get_llm_response(user_input)
        if text_response:
            print("\nAssistant:", text_response)
            
            # Generate and save audio
            audio_file = generate_speech(text_response)
            
            # Save assistant response to chat history
            save_chat_history(chat_file, "Assistant", text_response, audio_file)
            
            if audio_file:
                print(f"\nAudio response saved to: {audio_file}")
        else:
            error_msg = "Sorry, I couldn't generate a response. Please try again."
            print("\n" + error_msg)
            save_chat_history(chat_file, "System", error_msg)

if __name__ == "__main__":
    chat()
