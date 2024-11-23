# Conda: renew_project
from openai import OpenAI

openai.api_key=""

# Initialize the OpenAI client
client = OpenAI(
    api_key=openai.api_key  # Add your API key here
)

# Create chat completion
completion = client.chat.completions.create(
    model="gpt-4o",  # or gpt-3.5-turbo
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ],
    temperature=0.5,
    max_tokens=1024
)

print(completion.choices[0].message.content)