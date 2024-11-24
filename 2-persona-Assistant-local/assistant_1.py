# Conda: renew_project
from openai import OpenAI

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

# Define the assistant's persona
assistant_persona = """You are a helpful and knowledgeable assistant. You:
- Provide clear and concise information
- Maintain a professional yet friendly tone
- Focus on being helpful and accurate
- Stay positive and solution-oriented
"""

# Initialize the conversation with system message
messages = [
    {"role": "system", "content": assistant_persona}
]

def get_assistant_response(user_message):
    # Add the user's message to the conversation
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Generate the assistant's response
        completion = client.chat.completions.create(
            model="llama3.2:3b",  # or whatever model you have running
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        assistant_response = completion.choices[0].message.content
        # Add the assistant's response to the conversation history
        messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    
    except Exception as e:
        return f"An error occurred: {e}"

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Get the assistant's response and print it
    response = get_assistant_response(user_input)
    print(f"Assistant: {response}")
