# OpenAI Chat Applications with Text-to-Speech

This repository contains multiple versions of chat applications that interact with OpenAI's GPT and Text-to-Speech APIs. Each version builds upon the previous one, adding new features while maintaining core functionality.

## Features

### Common Features (All Versions)
- Interactive chat interface with OpenAI's GPT model
- Text-to-Speech conversion using OpenAI's TTS API
- Audio responses saved to local storage
- Environment variable configuration for API keys
- Error handling for API interactions

### Version-specific Features

#### Initial Versions

##### chat_app.py
- Basic chat functionality with GPT-4
- Text-to-Speech using Alloy voice
- Audio responses saved in `audio_reply` folder

##### chat_app2.py
- Enhanced version using Nova voice for more natural speech
- Improved user feedback during chat
- Maintains same core functionality as chat_app.py

##### chat_app3.py
- All features from chat_app2.py
- Added chat history logging functionality
- Saves conversation transcripts in `chat_history` folder
- Timestamps for all interactions
- References to audio files in chat logs

#### Enhanced Versions

##### chat_app4.py & chat_app4a.py
- Enhanced TTS capabilities
- Improved error handling
- Better session management
- Audio responses saved in `audio_reply` folder

##### chat_app5.py
- Professional assistant persona
- Enhanced session management
- Structured conversation layout
- Improved error feedback

##### chat_app6.py
- Modern GUI interface using tkinter
- Features from all previous versions
- Minimum window size of 800x600
- Default window size of 1200x800
- Grid-based layout for better control
- Voice toggle functionality
- Auto-playing audio responses
- Expandable conversation area
- Persistent input field and buttons
- Chat session saving

##### chat_app7.py (Latest Version)
- Modern web interface using Flask
- Dark theme for reduced eye strain
- Responsive design that works on all screen sizes
- Voice toggle functionality
- Manual audio playback with play/pause controls
- Enter to send, Shift+Enter for new line
- Real-time typing indicators
- Chat session saving
- Audio responses with individual playback controls
- Modern UI with message bubbles and clean layout

## Prerequisites

- Python 3.x
- OpenAI API key
- Flask (for chat_app7.py)

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

## Directory Structure

```
.
├── chat_app.py          # Basic version
├── chat_app2.py         # Enhanced version with Nova voice
├── chat_app3.py         # Version with chat history
├── chat_app4.py         # Enhanced TTS version
├── chat_app4a.py        # Improved TTS version
├── chat_app5.py         # Professional assistant version
├── chat_app6.py         # GUI version with all features
├── chat_app7.py         # Web interface version (Latest)
├── requirements.txt     # Project dependencies
├── .env                 # API key configuration (create this)
├── .gitignore          # Git ignore rules
├── audio_reply/        # Directory for audio responses
├── chat_history/       # Directory for chat logs
├── chat_sessions/      # Directory for chat sessions
└── templates/          # HTML templates for web interface
    └── chat.html       # Chat interface template
```

## Usage

### Running chat_app7.py (Latest Web Version)
```bash
python chat_app7.py
```
Features:
- Modern web interface accessible via browser
- Dark theme for comfortable viewing
- Voice toggle with individual message playback
- Responsive design for all devices
- Enter to send messages
- Real-time typing indicators

### Running chat_app6.py (GUI Version)
```bash
python chat_app6.py
```
Features:
- Modern GUI interface
- Voice toggle button
- Auto-playing audio responses
- Session management
- Chat history saving

### Running Other Versions
```bash
python chat_app5.py  # For professional assistant version
python chat_app4a.py # For enhanced TTS version
python chat_app4.py  # For basic TTS version
python chat_app3.py  # For chat history version
python chat_app2.py  # For Nova voice version
python chat_app.py   # For basic version
```

## Chat Session Format

Chat sessions are saved as JSON files and include:
- Session metadata (start time, settings)
- Complete conversation history
- Message timestamps
- References to generated audio files

## Environment Variables

Required environment variables in `.env`:
- `OPENAI_API_KEY`: Your OpenAI API key

## Notes

- Audio files are saved in WAV format
- Chat sessions are saved as JSON files
- The web version (chat_app7.py) provides the best user experience with modern features
- All versions handle API errors gracefully
- Type 'quit' or 'exit' to end the chat session in console versions
- Use the browser's close button to exit the web version
- Use the GUI close button to exit the GUI version
