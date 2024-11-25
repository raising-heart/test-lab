# AI Digital Assistant (A.I.D.A.)

A sophisticated AI chatbot implementation using Chainlit and local LLM (Ollama) integration. This project showcases different versions of A.I.D.A. (Artificial Intelligent Digital Assistant) with varying capabilities and personalities.

## Project Structure

The project contains multiple implementations of A.I.D.A., each with different features and improvements:

### Core Files

1. `aida.py` - Base implementation
   - Basic chatbot functionality
   - Integration with Ollama LLM
   - Simple conversation management
   - Professional and respectful persona

2. `aida2.py` - Enhanced version with logging
   - Advanced conversation logging system
   - Graceful shutdown handling
   - Signal handling for clean termination
   - Conversation history tracking
   - File-based logging with timestamps

3. `aida3.py` - Professional assistant
   - Enhanced professional persona
   - Improved conversation management
   - Expert guidance capabilities
   - Welcome message implementation
   - Focus on technical and professional assistance

4. `aida4.py` - Curious and enthusiastic version
   - Engaging and enthusiastic personality
   - Enhanced conversation streaming
   - Improved error handling
   - Focus on learning and knowledge sharing
   - Interactive welcome message

5. `aida5.py` - Advanced system management
   - System management capabilities
   - Enhanced AI capabilities
   - Research and analysis features
   - Blueprint creation functionality
   - Specialized persona with unique features

6. `aida6.py` - Voice-enabled version with enhanced storage
   - All features from aida4.py
   - Voice responses using OpenAI's text-to-speech
   - JSON-based chat session storage
   - Audio file management
   - Complete conversation tracking
   - Real-time streaming with audio playback

### Storage Directories

- `conversation_logs/` - Text-based conversation logs
- `audio_reply/` - Stores generated audio response files
- `chat_sessions/` - Contains JSON files of complete chat sessions

## Common Features Across All Versions

- Integration with Ollama LLM (llama3.2:3b model)
- Chainlit-based web interface
- Real-time response streaming
- Conversation history management
- Error handling and recovery
- Professional AI assistant capabilities

## Technical Requirements

- Python 3.x
- Ollama running locally (endpoint: http://localhost:11434/v1)
- Required Python packages:
  - chainlit
  - openai
  - python-dotenv (for aida6.py)
  - logging (standard library)
  - os (standard library)
  - datetime (standard library)
- OpenAI API key (required for aida6.py voice features)

## Getting Started

1. Ensure Ollama is running locally
2. Install required dependencies
3. For aida6.py, create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Choose the desired version of A.I.D.A.
5. Run using Chainlit:
   ```bash
   chainlit run [chosen_version].py
   ```

## Features by Version

### aida.py (Base Version)
- Basic conversation capabilities
- Simple system message handling
- Streamlined response generation

### aida2.py (Logging Version)
- Comprehensive logging system
- Conversation tracking with timestamps
- Clean shutdown mechanisms
- Signal handling for termination

### aida3.py (Professional Version)
- Enhanced professional responses
- Technical expertise focus
- Improved conversation management
- Welcome message implementation

### aida4.py (Enthusiastic Version)
- Engaging personality
- Learning-focused interactions
- Enhanced streaming capabilities
- Improved error handling

### aida5.py (Advanced Version)
- System management capabilities
- Research and analysis features
- Blueprint creation
- Enhanced AI capabilities

### aida6.py (Voice-Enabled Version)
- Text-to-speech responses
- Audio playback in chat interface
- Structured JSON chat history
- Complete session management
- Timestamp-based file organization

## Logging and Storage

### Text Logs
- Conversation logs stored in the `conversation_logs` directory
- Timestamps for easy reference and debugging

### JSON Chat Sessions (aida6.py)
Chat sessions are stored in JSON format with the following structure:
```json
{
  "session_id": "YYYYMMDD_HHMMSS",
  "start_time": "ISO timestamp",
  "end_time": "ISO timestamp",
  "messages": [
    {
      "role": "user/assistant",
      "content": "message content",
      "timestamp": "ISO timestamp",
      "audio_file": "path to audio file (for assistant messages)"
    }
  ]
}
```

### Audio Files
- Voice responses stored in `audio_reply` directory
- WAV format audio files
- Timestamp-based naming for easy tracking

## Contributing

Feel free to contribute to this project by:
- Implementing new features
- Improving existing functionality
- Enhancing the conversation capabilities
- Adding new AI assistant versions

## Note

This project demonstrates different approaches to implementing an AI assistant, each with its own unique features and capabilities. Choose the version that best suits your needs or use them as a reference for building your own AI assistant implementation. The latest addition (aida6.py) extends the functionality with voice responses and structured data storage.
