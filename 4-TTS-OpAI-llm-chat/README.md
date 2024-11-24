# OpenAI Chat Applications with Text-to-Speech

This repository contains three versions of a chat application that interacts with OpenAI's GPT and Text-to-Speech APIs. Each version builds upon the previous one, adding new features while maintaining core functionality.

## Features

### Common Features (All Versions)
- Interactive chat interface with OpenAI's GPT model
- Text-to-Speech conversion using OpenAI's TTS API
- Audio responses saved to local storage
- Environment variable configuration for API keys
- Error handling for API interactions

### Version-specific Features

#### chat_app.py
- Basic chat functionality with GPT-4o
- Text-to-Speech using Alloy voice
- Audio responses saved in `audio_reply` folder

#### chat_app2.py
- Enhanced version using Nova voice for more natural speech
- Improved user feedback during chat
- Maintains same core functionality as chat_app.py

#### chat_app3.py
- All features from chat_app2.py
- Added chat history logging functionality
- Saves conversation transcripts in `chat_history` folder
- Timestamps for all interactions
- References to audio files in chat logs

## Prerequisites

- Python 3.x
- Conda environment: `renew_project`
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Running chat_app.py (Basic Version)
```bash
python chat_app.py
```
- Uses Alloy voice for TTS
- Saves audio in `audio_reply` folder

### Running chat_app2.py (Nova Voice Version)
```bash
python chat_app2.py
```
- Uses Nova voice for more natural speech
- Saves audio in `audio_reply` folder

### Running chat_app3.py (Full Featured Version)
```bash
python chat_app3.py
```
- Uses Nova voice for speech
- Saves audio in `audio_reply` folder
- Creates chat logs in `chat_history` folder

## Directory Structure

```
.
├── chat_app.py          # Basic version with Alloy voice
├── chat_app2.py         # Enhanced version with Nova voice
├── chat_app3.py         # Full version with chat history
├── requirements.txt     # Project dependencies
├── .env                 # API key configuration (create this)
├── .gitignore          # Git ignore rules
├── audio_reply/        # Directory for saved audio responses
└── chat_history/       # Directory for chat logs (chat_app3.py only)
```

## Chat History Format (chat_app3.py)

Chat history files are saved with timestamps and include:
- Session start and end times
- User messages with timestamps
- Assistant responses with timestamps
- References to generated audio files
- Clear separators between messages

Example:
```
Chat Session Started: 2024-01-01 12:34:56
--------------------------------------------------

[2024-01-01 12:34:58] User: Hello, how are you?
--------------------------------------------------

[2024-01-01 12:35:00] Assistant: I'm doing well, thank you for asking!
[2024-01-01 12:35:00] Audio saved to: audio_reply/response_20240101_123500.wav
--------------------------------------------------
```

## Environment Variables

Required environment variables in `.env`:
- `OPENAI_API_KEY`: Your OpenAI API key

## Notes

- Audio files are saved in WAV format
- Each chat session creates a new timestamped file in the chat history
- The applications handle API errors gracefully
- Type 'quit' or 'exit' to end the chat session
