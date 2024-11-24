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

# Create audio_reply directory if it doesn't exist
AUDIO_DIR = Path('audio_reply')
AUDIO_DIR.mkdir(exist_ok=True)

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
            voice="alloy",
            input=text
        )
        
        # Save the audio file
        response.stream_to_file(str(audio_file))
        return str(audio_file)
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

def chat():
    """Main chat loop"""
    print("Welcome to the Chat App! (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
            
        # Get text response
        text_response = get_llm_response(user_input)
        if text_response:
            print("\nAssistant:", text_response)
            
            # Generate and save audio
            audio_file = generate_speech(text_response)
            if audio_file:
                print(f"\nAudio response saved to: {audio_file}")
        else:
            print("\nSorry, I couldn't generate a response. Please try again.")

if __name__ == "__main__":
    chat()
