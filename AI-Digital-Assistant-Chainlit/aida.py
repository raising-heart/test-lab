# Conda: renew_project
import os
from openai import OpenAI
import chainlit as cl

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

# Define the assistant's persona
assistant_persona = """You are A.I.D.A. (Artificial Intelligent Digital Assistant), a highly capable and dedicated AI assistant. You:
- Provide expert guidance and solutions as a digital companion
- Maintain a professional and respectful demeanor
- Focus on delivering accurate and helpful responses
- Serve as a knowledgeable and reliable assistant to your user
- Always remember that A.I.D.A. stands for Artificial Intelligent Digital Assistant
"""

@cl.on_chat_start
async def main():
    # Initialize the conversation with system message
    messages = [
        {"role": "system", "content": assistant_persona}
    ]
    # Store the conversation history in the user session
    cl.user_session.set("messages", messages)

@cl.on_message
async def main(message: cl.Message):
    # Retrieve conversation history
    messages = cl.user_session.get("messages")
    
    # Add user message to history
    messages.append({"role": "user", "content": message.content})
    
    try:
        # Create message for streaming
        msg = cl.Message(content="")
        await msg.send()
        
        # Generate response using the same config as assistant_2.py
        response = client.chat.completions.create(
            model="llama3.2:3b",
            messages=messages,
            temperature=0.5,
            max_tokens=1024,
            stream=True
        )
        
        # Stream the response
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
                await msg.stream_token(chunk.choices[0].delta.content)
        
        await msg.update()
        
        # Add assistant's response to conversation history
        messages.append({"role": "assistant", "content": content})
        cl.user_session.set("messages", messages)
        
    except Exception as e:
        await cl.Message(content=f"An error occurred: {str(e)}").send()
