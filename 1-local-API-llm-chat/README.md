# Local LLM Chat Application

This repository contains a set of Python scripts for interacting with both local and remote Large Language Models (LLMs).

## Files Description

### 1. `api_llm.py`
A simple script that demonstrates how to interact with OpenAI's API. This script:
- Uses the OpenAI Python client library
- Requires an OpenAI API key
- Makes a single request to generate a haiku about recursion
- Suitable for testing API connectivity and basic interactions

### 2. `local_llm.py`
A script for interacting with locally hosted LLM models using Ollama. Features:
- Connects to a local LLM server (default: http://localhost:11434/v1)
- No API key required
- Uses the llama3.2:3b model (configurable)
- Demonstrates basic prompt completion with local models

### 3. `local_llm_chat.py`
An interactive chat application using local LLM models. This script:
- Provides a continuous chat interface in the terminal
- Maintains conversation history
- Uses the local Ollama server
- Supports back-and-forth dialogue with the model
- Exit the chat by typing 'exit'

## Requirements
- Python 3.x
- OpenAI Python package
- Ollama (for local LLM functionality)
- Active internet connection (for `api_llm.py`)
- Local LLM server running (for `local_llm.py` and `local_llm_chat.py`)

## Setup
1. Install the required Python package:
   ```bash
   pip install openai
   ```
2. For `api_llm.py`: Add your OpenAI API key to the script
3. For local LLM scripts: Ensure Ollama is installed and running with the desired model

## Usage
Each script can be run directly using Python:
```bash
python api_llm.py      # For OpenAI API interaction
python local_llm.py    # For single local LLM interaction
python local_llm_chat.py # For interactive chat session
```
