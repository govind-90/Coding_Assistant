# Code Assistant for VS Code

A modular, production-ready code assistant for Visual Studio Code, featuring a FastAPI backend (Python, LangChain, Gemini) and a VS Code extension frontend. Supports two modes:
- **Edit**: Context-aware file editing with chat confirmation and explanation.
- **Ask**: Conversational Q&A about your codebase, with or without a tagged file.

## Features
- **Edit Mode**: AI-powered, context-aware code editing for any tagged file in your workspace.
- **Ask Mode**: Conversational Q&A about your codebase, with persistent chat history.
- **Persistent Memory**: Chat history is stored locally in VS Code and passed to the backend for context.
- **WebSocket Communication**: Real-time, low-latency interaction between extension and backend.
- **Minimal, Clean Architecture**: Only essential files and dependencies included.

## Project Structure
```
Backend/
  chains/         # LLM prompt chains for 'edit' and 'ask' modes
  controllers/    # FastAPI routers for chat and mode handling
  services/       # Service logic for edit/ask, context formatting
  tools/          # Context extraction and file utilities
  utils/          # Language inference
  config.py       # API key and model config
  main.py         # FastAPI app entry point
Frontend/
  src/extension.ts  # Main VS Code extension logic
  package.json      # Extension manifest and dependencies
  dist/             # Compiled extension output
```

## Setup Instructions

### 1. Backend (FastAPI + LangChain + Gemini)
#### Prerequisites
- Python 3.10+
- Google Gemini API key (set in `.env` as `GOOGLE_API_KEY`)

#### Install dependencies
```sh
pip install -r requirements.txt
```

#### Run the backend server
```sh
uvicorn Backend.main:app --reload
```

### 2. VS Code Extension (Frontend)
#### Prerequisites
- Node.js 18+
- VS Code 1.104.0+

#### Install dependencies and build
```sh
cd Frontend
npm install
npm run compile
```

#### Load the extension in VS Code
1. Open VS Code, go to the Extensions sidebar, click 'Run Extension' (F5) or use the debugger.
2. Use the command palette (`Ctrl+Shift+P`) and run `Code Assistant: Open Chat`.

## Usage
- **Tag a file**: Click 'Tag File' in the chat panel to select a file for context-aware editing.
- **Edit Mode**: Enter an instruction and select 'Edit' to update the tagged file with AI.
- **Ask Mode**: Enter a question and select 'Ask' to get explanations or code help.
- **Chat History**: All interactions are stored and used for context in future requests.

## Architecture Overview
- **Backend**: FastAPI app exposes a WebSocket endpoint. Handles 'edit' and 'ask' modes using LangChain and Gemini. Context and chat history are always included in prompts.
- **Frontend**: VS Code extension provides a chat UI, manages persistent chat history, and communicates with the backend via WebSocket.

## Dependencies
### Backend
- fastapi
- uvicorn
- langchain
- langchain-google-genai
- python-dotenv

### Frontend
- ws (WebSocket client)
- typescript, @types/node, @types/vscode (dev)

## License
MIT

---
*Last updated: September 18, 2025*
