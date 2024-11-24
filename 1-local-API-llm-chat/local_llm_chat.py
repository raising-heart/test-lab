# Conda: renew_project
from openai import OpenAI

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="not_required"
)

messages = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
        
    messages.append({"role": "user", "content": user_input})
    
    completion = client.chat.completions.create(
        model="llama3.2:3b",  # or whatever model you have running in Ollama
        messages=messages,
        temperature=0.5,
        max_tokens=1024
    )
    
    assistant_response = completion.choices[0].message.content
    print("Assistant:", assistant_response)
    messages.append({"role": "assistant", "content": assistant_response})