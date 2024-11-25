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
    def __init__(self, model="llama3.2:3b", temperature=0.7, max_tokens=300, voice="nova"):
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
        
        # Define the assistant's persona (using assistant_2.py style)
        self.assistant_persona = """You are a highly capable and dedicated AI assistant. You:
        - Provide expert guidance and solutions
        - Maintain a professional and respectful demeanor
        - Focus on delivering accurate and helpful responses
        - Serve as a knowledgeable companion to your user
        - Communicate clearly and effectively
        - Adapt to the user's needs and preferences
        """
        
        # Initialize conversation history with initial exchange
        self.messages = [
            {"role": "system", "content": self.assistant_persona},
            {"role": "user", "content": "I am your user, and you are my dedicated AI assistant"},
            {"role": "assistant", "content": "I am here to assist you. I'll provide expert guidance while maintaining professionalism and accuracy in our interactions. How may I help you today?"}
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
        
        session_data = {
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'voice': self.voice,
            'messages': self.messages[1:],  # Exclude system message
            'session_info': {
                'start_time': self.session_start_time,
                'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_exchanges': len(self.messages) // 2  # Approximate number of exchanges
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2)
        
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

    def display_welcome_message(self):
        """Display welcome message with session information"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"Welcome to AI Assistant v5.0!")
        print(f"{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Session Information:")
        print(f"- Model: {self.model}")
        print(f"- Voice: {self.voice}")
        print(f"- Temperature: {self.temperature}")
        print(f"- Max Tokens: {self.max_tokens}")
        print(f"- Audio Directory: {self.audio_dir}")
        print(f"- Session Directory: {self.chat_sessions_dir}")
        print(f"\nType 'exit' or 'quit' to end the session")
        print(f"{'='*50}{Style.RESET_ALL}\n")

    def start_chat(self):
        """Start the interactive chat session"""
        self.session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.display_welcome_message()
        
        while True:
            # Get user input with colored prompt
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye"]:
                # Save session before exiting
                session_file = self.save_session()
                print(f"\n{Fore.YELLOW}Session saved to: {session_file}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Thank you for using AI Assistant. Goodbye!{Style.RESET_ALL}")
                break
            
            if not user_input.strip():  # Skip empty inputs
                continue
            
            # Get and display assistant response
            response, audio_file = self.get_assistant_response(user_input)
            print(f"\n{Fore.BLUE}Assistant: {Style.RESET_ALL}{response}\n")
            
            if audio_file:
                print(f"{Fore.YELLOW}Audio response saved to: {audio_file}{Style.RESET_ALL}\n")

def main():
    try:
        assistant = ChatAssistant()
        assistant.start_chat()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Session interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
    finally:
        print(f"\n{Fore.CYAN}Session ended. Thank you for using AI Assistant!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
