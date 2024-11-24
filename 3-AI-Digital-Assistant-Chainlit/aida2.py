# Conda: renew_project
import os
from openai import OpenAI
import chainlit as cl
from datetime import datetime
import logging
import atexit
import signal
import sys

# Set up logging
log_directory = "conversation_logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a unique log file name with timestamp
log_file = os.path.join(log_directory, f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Configure logging with a file handler
file_handler = logging.FileHandler(log_file, mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s\n%(message)s\n', datefmt='%Y-%m-%d %H:%M:%S'))

# Get the logger
logger = logging.getLogger('conversation_logger')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def cleanup():
    """Cleanup function to be called on exit"""
    logger.info("\nConversation ended")
    file_handler.flush()
    file_handler.close()

# Register cleanup function
atexit.register(cleanup)

# Signal handler for graceful shutdown
def signal_handler(signum, frame):
    shutdown_message = "\n\nProgram terminated. Saving conversation logs..."
    print(shutdown_message)
    logger.info(shutdown_message)
    cleanup()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

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

Current conversation:
{history}
{question}"""

@cl.on_chat_start
async def main():
    logger.info("Starting new conversation session")
    
    # Initialize the conversation with system message
    messages = [
        {"role": "system", "content": assistant_persona}
    ]
    conversation_history = ""
    # Store in the user session
    cl.user_session.set("messages", messages)
    cl.user_session.set("conversation_history", conversation_history)

@cl.on_message
async def main(message: cl.Message):
    # Check for exit command
    if message.content.lower() in ['/exit', '/quit', '/bye']:
        logger.info("Exit command received")
        await cl.Message(content="Goodbye! Saving conversation and closing... You can now close the browser window and press Ctrl+C in the terminal to exit completely.").send()
        cleanup()
        return

    # Retrieve conversation history and messages
    messages = cl.user_session.get("messages")
    conversation_history = cl.user_session.get("conversation_history")
    
    # Format the system message with current context
    current_context = assistant_persona.format(
        history=conversation_history,
        question=f"Question: {message.content}" if message.content else ""
    )
    messages[0]["content"] = current_context
    
    # Print and log the current context
    context_message = f"\nCurrent LLM Context:\n-------------------\n{current_context}\n-------------------\n"
    print(context_message)
    logger.info(context_message)
    file_handler.flush()
    
    # Add user message to messages list
    messages.append({"role": "user", "content": message.content})
    
    try:
        # Create message for streaming
        msg = cl.Message(content="")
        await msg.send()
        
        # Generate response
        response = client.chat.completions.create(
            model="llama3.2:3b",
            messages=messages,
            temperature=0.5,
            max_tokens=1024,
            stream=True
        )
        
        # Log the API request
        logger.info(f"HTTP Request: POST http://localhost:11434/v1/chat/completions")
        file_handler.flush()
        
        # Stream the response
        content = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content += chunk.choices[0].delta.content
                await msg.stream_token(chunk.choices[0].delta.content)
        
        # Update conversation history with the Q&A pair
        conversation_history += f"Question: {message.content}\n"
        conversation_history += f"Answer: {content}\n"
        
        # Print and log the updated context
        updated_context = assistant_persona.format(
            history=conversation_history,
            question=""
        ).rstrip()
        response_message = f"\nUpdated Context After Response:\n-------------------\n{updated_context}\n-------------------\n"
        print(response_message)
        logger.info(response_message)
        file_handler.flush()
        
        # Add assistant's response to messages
        messages.append({"role": "assistant", "content": content})
        
        # Update the message
        await msg.update()
        
        # Save updated histories
        cl.user_session.set("messages", messages)
        cl.user_session.set("conversation_history", conversation_history)
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.error(error_message)
        file_handler.flush()
        await cl.Message(content=error_message).send()

@cl.on_stop
async def on_stop():
    logger.info("\nConversation ended by user")
    file_handler.flush()
