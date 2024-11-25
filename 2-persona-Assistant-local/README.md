# AI Assistant Implementation

This repository contains different implementations of an AI assistant using the Ollama local LLM service. Each implementation offers different interfaces and features while maintaining the core functionality of an AI assistant.

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

### `assistant_4.py`
A modern web-based implementation of the AI assistant using Flask that:
- Features a clean, modern web interface
- Provides real-time chat interactions
- Includes typing indicators and smooth animations
- Offers a responsive design that works on all screen sizes
- Maintains chat history during the session
- Supports markdown text formatting in messages

## Setup and Requirements

### Prerequisites
1. Python 3.x
2. Ollama running locally on port 11434

### Installation
1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### CLI and GUI Versions
Run any of the standalone versions:
```bash
python assistant_1.py  # Basic CLI version
python assistant_2.py  # Enhanced CLI version
python assistant_3.py  # GUI version
```

### Web Version (assistant_4)
To run the web-based version:
```bash
python -m flask --app assistant_4.py run
```
Then open your browser and navigate to `http://localhost:5000`

## Technical Details

- All assistants use the Ollama API (OpenAI-compatible)
- Default model: llama3.2:3b
- Web interface built with Flask and modern CSS
- Responsive design using Tailwind CSS
- Real-time message updates and typing indicators
- Cross-browser compatible
