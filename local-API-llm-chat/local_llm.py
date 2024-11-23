# Conda: renew_project
from openai import OpenAI

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="not_required"
)

# Create chat completion
completion = client.chat.completions.create(
    model="llama3.2:3b",  # or whatever model you have running in Ollama
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ],
    temperature=0.5,
    max_tokens=1024
)

print(completion.choices[0].message.content)