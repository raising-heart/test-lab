# Conda: renew_project
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from openai import OpenAI
import json
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv
import threading
from playsound import playsound

# Load environment variables
load_dotenv()

class ChatAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.initialize_assistant()
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Configure the main window
        self.root.title("AI Assistant Chat v6.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Create main container with grid
        main_container = ttk.Frame(self.root)
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)  # Make conversation area expandable
        main_container.grid_columnconfigure(0, weight=1)  # Make columns expandable
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create top info frame
        info_frame = ttk.Frame(main_container)
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Add status indicators
        self.model_label = ttk.Label(info_frame, text="Model: llama3.2:3b")
        self.model_label.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(info_frame, text="Status: Ready")
        self.status_label.pack(side=tk.RIGHT)
        
        # Create conversation frame
        conversation_frame = ttk.Frame(main_container)
        conversation_frame.grid(row=1, column=0, sticky="nsew")
        conversation_frame.grid_rowconfigure(0, weight=1)
        conversation_frame.grid_columnconfigure(0, weight=1)
        
        # Create conversation display
        self.conversation_text = scrolledtext.ScrolledText(
            conversation_frame,
            wrap=tk.WORD,
            font=("Arial", 20),
            bg='white',
            fg='black'
        )
        self.conversation_text.grid(row=0, column=0, sticky="nsew")
        
        # Create bottom frame for input
        input_frame = ttk.Frame(main_container)
        input_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        input_frame.grid_columnconfigure(0, weight=1)  # Make input field expandable
        
        # Create input field
        self.user_input = ttk.Entry(
            input_frame,
            font=("Arial", 20)
        )
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.user_input.bind('<Return>', lambda e: self.send_message())
        
        # Create buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=0, column=1, sticky="e")
        
        # Create send button
        self.send_button = ttk.Button(
            buttons_frame,
            text="Send",
            command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Create voice toggle button
        self.voice_enabled = tk.BooleanVar(value=True)
        self.voice_button = ttk.Checkbutton(
            buttons_frame,
            text="Voice",
            variable=self.voice_enabled
        )
        self.voice_button.pack(side=tk.LEFT, padx=5)
        
        # Create clear button
        self.clear_button = ttk.Button(
            buttons_frame,
            text="Clear",
            command=self.clear_conversation
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Configure style
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TFrame', background='#f0f0f0')
        
    def initialize_assistant(self):
        """Initialize the chat assistant components"""
        # Create necessary directories
        self.audio_dir = Path('audio_reply')
        self.chat_sessions_dir = Path('chat_sessions')
        self.audio_dir.mkdir(exist_ok=True)
        self.chat_sessions_dir.mkdir(exist_ok=True)
        
        # Initialize OpenAI clients
        self.local_client = OpenAI(
            base_url="http://localhost:11434/v1",  # Ollama
            api_key="not_required"
        )
        
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize chat settings
        self.model = "llama3.2:3b"
        self.temperature = 0.7
        self.max_tokens = 300
        self.voice = "nova"
        
        # Initialize conversation history
        self.messages = [
            {"role": "system", "content": self.get_assistant_persona()},
            {"role": "user", "content": "I am your user, and you are my dedicated AI assistant"},
            {"role": "assistant", "content": "I am here to assist you. How may I help you today?"}
        ]
        
        # Display welcome message
        self.display_welcome_message()
        
    def get_assistant_persona(self):
        """Return the assistant's persona"""
        return """You are a highly capable and dedicated AI assistant. You:
        - Provide expert guidance and solutions
        - Maintain a professional and respectful demeanor
        - Focus on delivering accurate and helpful responses
        - Serve as a knowledgeable companion to your user
        - Communicate clearly and effectively
        - Adapt to the user's needs and preferences
        """
        
    def display_welcome_message(self):
        """Display welcome message in the conversation"""
        welcome_msg = f"""Welcome to AI Assistant v6.0!
        
Current Settings:
- Model: {self.model}
- Voice: {self.voice}
- Temperature: {self.temperature}
- Max Tokens: {self.max_tokens}

The conversation will be saved automatically when you close the application.
Audio responses will be saved in the '{self.audio_dir}' directory.

How may I assist you today?

{'='*50}
"""
        self.conversation_text.insert(tk.END, welcome_msg)
        
    def generate_speech(self, text):
        """Generate speech from text using OpenAI's TTS"""
        try:
            if not self.voice_enabled.get():
                return None
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = self.audio_dir / f"response_{timestamp}.wav"
            
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text
            )
            
            # Save the audio file
            response.stream_to_file(str(audio_file))
            
            # Play the audio in a separate thread
            threading.Thread(target=self.play_audio, args=(str(audio_file),), daemon=True).start()
            
            return str(audio_file)
            
        except Exception as e:
            self.show_error(f"Error generating speech: {str(e)}")
            return None
            
    def play_audio(self, audio_file):
        """Play the audio file"""
        try:
            playsound(audio_file)
        except Exception as e:
            self.root.after(0, self.show_error, f"Error playing audio: {str(e)}")
            
    def send_message(self):
        """Handle sending a message"""
        user_input = self.user_input.get().strip()
        if not user_input:
            return
            
        # Clear input field
        self.user_input.delete(0, tk.END)
        
        # Display user message
        self.conversation_text.insert(tk.END, f"\nYou: {user_input}\n")
        self.conversation_text.see(tk.END)
        
        # Disable input while processing
        self.toggle_input(False)
        
        # Process message in a separate thread
        threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()
        
    def process_message(self, user_input):
        """Process the user message and generate response"""
        try:
            # Add user message to history
            self.messages.append({"role": "user", "content": user_input})
            
            # Generate response
            completion = self.local_client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            assistant_response = completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_response})
            
            # Display assistant response
            self.root.after(0, self.display_response, assistant_response)
            
            # Generate speech in background
            if self.voice_enabled.get():
                audio_file = self.generate_speech(assistant_response)
                if audio_file:
                    self.root.after(0, self.display_audio_info, audio_file)
                    
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
        finally:
            # Re-enable input
            self.root.after(0, self.toggle_input, True)
            
    def display_response(self, response):
        """Display assistant response in the conversation"""
        self.conversation_text.insert(tk.END, f"\nAssistant: {response}\n")
        self.conversation_text.see(tk.END)
        
    def display_audio_info(self, audio_file):
        """Display audio file information"""
        self.conversation_text.insert(tk.END, f"\n[Audio saved to: {audio_file}]\n")
        self.conversation_text.see(tk.END)
        
    def toggle_input(self, enabled):
        """Enable or disable input controls"""
        state = 'normal' if enabled else 'disabled'
        self.user_input.configure(state=state)
        self.send_button.configure(state=state)
        self.status_label.configure(text=f"Status: {'Ready' if enabled else 'Processing...'}")
        
    def clear_conversation(self):
        """Clear the conversation display"""
        self.conversation_text.delete(1.0, tk.END)
        self.display_welcome_message()
        
    def show_error(self, error_message):
        """Display error message"""
        messagebox.showerror("Error", error_message)
        
    def save_session(self):
        """Save the current session"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.chat_sessions_dir / f"chat_session_{timestamp}.json"
            
            session_data = {
                'model': self.model,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'voice': self.voice,
                'messages': self.messages[1:],  # Exclude system message
                'session_info': {
                    'end_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_exchanges': len(self.messages) // 2
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2)
                
            return filename
        except Exception as e:
            self.show_error(f"Error saving session: {str(e)}")
            return None

def main():
    root = tk.Tk()
    app = ChatAssistantGUI(root)
    
    # Save session on window close
    def on_closing():
        session_file = app.save_session()
        if session_file:
            messagebox.showinfo("Session Saved", f"Chat session saved to:\n{session_file}")
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
