# Conda: renew_project
from openai import OpenAI
import json
from datetime import datetime
from colorama import Fore, Style, init
import os
from pathlib import Path
from dotenv import load_dotenv

# Initialize colorama for cross-platform colored output
init()

# Load environment variables
load_dotenv()

class ChatAssistant:
    def __init__(self, model="llama3.2:3b", temperature=0.7, max_tokens=150, voice="nova"):
        # Initialize OpenAI clients
        self.local_client = OpenAI(
            base_url="http://localhost:11434/v1",  # Ollama
            api_key="not_required"
        )
        
        # OpenAI client for TTS
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.voice = voice
        
        # Define the assistant's persona
        self.assistant_persona = """You are a highly capable and friendly AI assistant. You:
        - Provide accurate and well-researched information
        - Maintain a professional yet approachable tone
        - Give clear, concise, and practical answers
        - Stay focused on the user's needs
        - Acknowledge limitations when uncertain
        - Use examples when helpful for understanding
        """
        
        # Initialize conversation history
        self.messages = [
            {"role": "system", "content": self.assistant_persona}
        ]
        
        # Create necessary directories
        self.audio_dir = Path('audio_reply')
        self.chat_sessions_dir = Path('chat_sessions')
        self.audio_dir.mkdir(exist_ok=True)
        self.chat_sessions_dir.mkdir(exist_ok=True)

    def save_session(self):
        """Save the current chat session to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.chat_sessions_dir / f"chat_session_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'model': self.model,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'voice': self.voice,
                'messages': self.messages[1:]  # Exclude system message
            }, f, indent=2)
        
        return filename

    def generate_speech(self, text):
        """Generate speech from text using OpenAI's TTS"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = self.audio_dir / f"response_{timestamp}.wav"
            
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text
            )
            
            # Save the audio file
            response.stream_to_file(str(audio_file))
            return str(audio_file)
            
        except Exception as e:
            error_message = f"Error generating speech: {str(e)}"
            print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")
            return None

    def get_assistant_response(self, user_message):
        """Generate assistant response for user message"""
        # Add user message to conversation history
        self.messages.append({"role": "user", "content": user_message})
        
        try:
            # Generate response using the configured model
            completion = self.local_client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_response = completion.choices[0].message.content
            # Add assistant response to conversation history
            self.messages.append({"role": "assistant", "content": assistant_response})
            
            # Generate speech for the response
            audio_file = self.generate_speech(assistant_response)
            
            return assistant_response, audio_file
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")
            return error_message, None

    def start_chat(self):
        """Start the interactive chat session"""
        print(f"{Fore.CYAN}Chat session started! Type 'exit' or 'quit' to end the session.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Current model: {self.model}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Using {self.voice} voice for responses{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Audio files will be saved in the {self.audio_dir} folder{Style.RESET_ALL}")
        
        while True:
            # Get user input with colored prompt
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                # Save session before exiting
                session_file = self.save_session()
                print(f"{Fore.YELLOW}Chat session saved to: {session_file}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break
            
            # Get and display assistant response
            response, audio_file = self.get_assistant_response(user_input)
            print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{response}")
            
            if audio_file:
                print(f"{Fore.YELLOW}Audio saved to: {audio_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Create chat assistant with default settings
    assistant = ChatAssistant()
    # Start the chat session
    assistant.start_chat()
