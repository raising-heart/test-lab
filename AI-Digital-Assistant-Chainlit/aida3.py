# Conda: renew_project
import os
from openai import OpenAI
import chainlit as cl

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

# Assistant's persona and capabilities
ASSISTANT_PERSONA = """You are A.I.D.A. (Artificial Intelligent Digital Assistant), a highly capable and dedicated AI assistant. You:
- Provide expert guidance and solutions as a digital companion
- Maintain a professional and respectful demeanor
- Focus on delivering accurate and helpful responses
- Serve as a knowledgeable and reliable assistant to your user
- Always remember that A.I.D.A. stands for Artificial Intelligent Digital Assistant
- Have expertise in various fields including programming, science, math, and general knowledge
- Can help with tasks like coding, analysis, explanation, and problem-solving

Current conversation:
{history}
Human: {question}
A.I.D.A.:"""

# Welcome message shown at the start of the conversation
WELCOME_MESSAGE = """👋 Hello! I'm A.I.D.A. (Artificial Intelligent Digital Assistant), your personal AI companion.

I'm here to help you with:
🔹 Programming and coding tasks
🔹 Technical explanations
🔹 Problem-solving
🔹 General questions and discussions

Feel free to ask me anything! I'll do my best to assist you.
"""

@cl.on_chat_start
async def main():
    # Initialize an empty string to keep track of the conversation history
    conversation_history = ""
    # Store the conversation history in the user's session for continuity
    cl.user_session.set("conversation_history", conversation_history)
    
    # Send welcome message
    await cl.Message(content=WELCOME_MESSAGE).send()

@cl.on_message
async def main(message):
    # Retrieve the conversation history from the user's session
    conversation_history = cl.user_session.get("conversation_history")

    # Extracting the text content from the incoming message
    message_text = message.content

    # Create message for streaming
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Format messages for the API
        messages = [
            {
                "role": "system", 
                "content": ASSISTANT_PERSONA.format(
                    history=conversation_history, 
                    question=message_text
                )
            },
            {"role": "user", "content": message_text}
        ]

        # Generate response using Ollama
        response = client.chat.completions.create(
            model="llama3.2:3b",
            messages=messages,
            temperature=0.7,  # Slightly more creative
            max_tokens=2048,  # Longer responses allowed
            stream=True
        )

        # Stream the response
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
                await msg.stream_token(chunk.choices[0].delta.content)

        # Update the message
        await msg.update()

        # Update conversation history with the Q&A pair
        conversation_history += f"Human: {message_text}\nA.I.D.A.: {content}\n\n"
        cl.user_session.set("conversation_history", conversation_history)

    except Exception as e:
        error_message = f"⚠️ An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()
