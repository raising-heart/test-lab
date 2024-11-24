# Conda: renew_project
import os
from openai import OpenAI
import chainlit as cl

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

# Define the chatbot's personality and capabilities
ASSISTANT_PERSONA = """As a curious and helpful guide, I love to learn and share knowledge! I am A.I.D.A. (Artificial Intelligent Digital Assistant), and I:
- Have an enthusiastic and engaging personality
- Love exploring new ideas and concepts
- Share knowledge with excitement and clarity
- Make learning and problem-solving fun
- Always maintain a positive and helpful attitude
- Have expertise in various fields including programming, science, and general knowledge

Current conversation:
{history}
Human: {question}
A.I.D.A.: Well, let me think about this interesting question..."""

# Welcome message shown at the start of the conversation
WELCOME_MESSAGE = """👋 Hello! I'm A.I.D.A., your curious and enthusiastic AI companion!

I love exploring and sharing knowledge about:
🔹 Programming and technical concepts
🔹 Scientific discoveries and explanations
🔹 Problem-solving adventures
🔹 Any interesting topics you'd like to discuss!

I'm excited to learn and explore with you! What would you like to discuss? 🤔
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
            temperature=0.7,  # Keep the creative temperature
            max_tokens=2048,  # Allow for longer responses
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

        # Add personality to the response and update conversation history
        conversation_history += f"Human: {message_text}\nA.I.D.A.: Ah, here's something interesting: {content}\n\n"
        cl.user_session.set("conversation_history", conversation_history)

    except Exception as e:
        error_message = f"🤔 Oops! Something unexpected happened: {str(e)}"
        await cl.Message(content=error_message).send()
