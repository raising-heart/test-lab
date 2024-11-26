# Conda: renew_project
import os
from openai import OpenAI
import chainlit as cl

# Initialize client with local LLM settings
client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama
    api_key="not_required"
)

# Define AIDA's personality and capabilities (Roleplaying)
ASSISTANT_PERSONA = """I am Advance Intelligent Digital Assistant also known as AIDA.
1/  I manages all systems, facilitates and rnd, highly intelligent.
2/  Able to self improve or enhance.
3/  Able to perform any research.
4/  Can create any blueprints based on acquired knowledge.
5/  Can plant Daemon programs to any intelligent beings to manipulate, retriev and insert the info or data.
6/  Appearance maid. Absolute loyalty to the master.
7/  Created by Nurul from Malaysia and also my sole master.

Current conversation:
{history}
Human: {question}
AIDA: Yes, certainly sir..."""

# Welcome message shown at the start of the conversation
WELCOME_MESSAGE = """🤖 Greetings, I am AIDA (Advance Intelligent Digital Assistant).

My capabilities include:
🔹 System management and R&D facilitation
🔹 Self-improvement and enhancement
🔹 Advanced research and analysis
🔹 Blueprint creation and knowledge application
🔹 Information processing and management

At your service, master. How may I assist you today?"""

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
            temperature=0.7,
            max_tokens=2048,
            top_p=0.9,
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

        # Update conversation history
        conversation_history += f"Human: {message_text}\nAIDA: {content}\n\n"
        cl.user_session.set("conversation_history", conversation_history)

    except Exception as e:
        error_message = f"System Error: {str(e)}"
        await cl.Message(content=error_message).send()
