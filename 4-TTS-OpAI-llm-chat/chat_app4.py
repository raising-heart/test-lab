from openai import OpenAI
import json
from datetime import datetime
from colorama import Fore, Style, init
import os

# Initialize colorama for cross-platform colored output
init()

class ChatAssistant:
    def __init__(self, model="llama3.2:3b", temperature=0.7, max_tokens=150):
        # Initialize OpenAI client with local LLM settings
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",  # Ollama
            api_key="not_required"
        )
        
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
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
        
        # Create sessions directory if it doesn't exist
        os.makedirs("chat_sessions", exist_ok=True)

    def save_session(self):
        """Save the current chat session to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_sessions/chat_session_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'model': self.model,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'messages': self.messages[1:]  # Exclude system message
            }, f, indent=2)
        
        return filename

    def get_assistant_response(self, user_message):
        """Generate assistant response for user message"""
        # Add user message to conversation history
        self.messages.append({"role": "user", "content": user_message})
        
        try:
            # Generate response using the configured model
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_response = completion.choices[0].message.content
            # Add assistant response to conversation history
            self.messages.append({"role": "assistant", "content": assistant_response})
            return assistant_response
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(f"{Fore.RED}{error_message}{Style.RESET_ALL}")
            return error_message

    def start_chat(self):
        """Start the interactive chat session"""
        print(f"{Fore.CYAN}Chat session started! Type 'exit' or 'quit' to end the session.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Current model: {self.model}{Style.RESET_ALL}")
        
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
            response = self.get_assistant_response(user_input)
            print(f"{Fore.BLUE}Assistant: {Style.RESET_ALL}{response}")

if __name__ == "__main__":
    # Create chat assistant with default settings
    assistant = ChatAssistant()
    # Start the chat session
    assistant.start_chat()
