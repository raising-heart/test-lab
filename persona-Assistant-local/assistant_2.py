# Conda: renew_project
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

# Loop conversation
while True:
    user_input = input("You: ")  # User input

    if user_input.lower() in ["exit", "quit", "bye"]:  # Exit the conversation
        break

    messages.append({"role": "user", "content": user_input})  # Add user input to memory
    
    try:
        # Generate response based on AI/LLM settings
        response = client.chat.completions.create(
            model="llama3.2:3b",  # or your preferred model
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        # Display assistant's response
        print("Assistant:", response.choices[0].message.content, "\n")
        
        # Update conversation memory
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        
    except Exception as e:
        print(f"An error occurred: {e}")
