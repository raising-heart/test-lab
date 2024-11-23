# Conda: renew_project
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from openai import OpenAI

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

# Initialize the conversation with system message
messages = [
    {"role": "system", "content": assistant_persona},
    {"role": "user", "content": "I am your user, and you are my dedicated AI assistant"}
]

def send_message():
    user_input = user_input_entry.get()
    if user_input.lower() in ["exit", "quit", "bye"]:  # Exit the conversation
        window.quit()
        return

    messages.append({"role": "user", "content": user_input})  # Add user input to memory

    try:
        # Generate response based on AI/LLM settings
        response = client.chat.completions.create(
            model="llama3.2:3b",  # or your preferred model
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        assistant_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_response})
        conversation_text.insert(tk.END, f"\nYou: {user_input}\n\nAssistant: {assistant_response}\n")
        user_input_entry.delete(0, tk.END)
    except Exception as e:
        conversation_text.insert(tk.END, f"\nError: {str(e)}\n")
        user_input_entry.delete(0, tk.END)

# Create the Tkinter window with rounded edges
window = tk.Tk()
window.title("AI Assistant Chat")
window.geometry("600x500")  # Slightly larger window for better readability

# Create a rounded edge frame to hold the conversation text
conversation_frame = ttk.Frame(window)
conversation_frame.place(relwidth=1, relheight=0.8)  # Increased height for more conversation space

# Create a text widget for displaying the conversation inside the rounded edge frame
conversation_text = scrolledtext.ScrolledText(conversation_frame, wrap=tk.WORD, font=("Arial", 20))
conversation_text.pack(fill=tk.BOTH, expand=True)

# Configure button style for larger text
style = ttk.Style()
style.configure('Large.TButton', font=("Arial", 20))

# Create an entry widget for user input with increased width and font size
user_input_entry = tk.Entry(window, width=50, font=("Arial", 20))
user_input_entry.place(relx=0.05, rely=0.85, relwidth=0.7, relheight=0.1)

# Create a send button with improved styling and larger text
send_button = ttk.Button(window, text="Send", command=send_message, style='Large.TButton')
send_button.place(relx=0.8, rely=0.85, relwidth=0.15, relheight=0.1)

# Bind Enter key to send_message function
window.bind('<Return>', lambda event: send_message())

# Start the GUI event loop
window.mainloop()
