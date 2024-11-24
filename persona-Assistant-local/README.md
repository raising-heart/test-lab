# AI Assistant Implementation

This repository contains three different implementations of an AI assistant using the Ollama local LLM service. Each implementation offers different interfaces and features while maintaining the core functionality of an AI assistant.

## Files Description

### `assistant_1.py`
A simple command-line interface (CLI) implementation of the AI assistant that:
- Uses the OpenAI-compatible API to communicate with Ollama
- Implements a basic chat loop for continuous interaction
- Features a professional yet friendly persona
- Includes basic error handling
- Limits responses to 150 tokens for concise interactions

### `assistant_2.py`
An enhanced command-line version of the AI assistant that:
- Extends the basic functionality of assistant_1
- Includes a more detailed conversation memory system
- Features an expanded token limit (300) for more detailed responses
- Implements a more sophisticated exit command system
- Maintains a professional and expert-focused persona

### `assistant_3.py`
A graphical user interface (GUI) version of the AI assistant built with Tkinter that:
- Provides a user-friendly graphical interface
- Features a scrollable conversation history
- Implements the same core AI functionality as assistant_2
- Offers a more polished user experience with a modern interface
- Includes visual feedback for user interactions

## Setup and Requirements

To run these assistants, you need:
1. Python 3.x
2. Ollama running locally on port 11434
3. The following Python packages:
   - openai
   - tkinter (for assistant_3.py)

## Usage

Each assistant can be run independently:
```bash
python assistant_1.py  # For basic CLI version
python assistant_2.py  # For enhanced CLI version
python assistant_3.py  # For GUI version
```

The assistants connect to a local Ollama instance and use the llama3.2:3b model by default.

