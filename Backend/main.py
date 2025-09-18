from fastapi import FastAPI, WebSocket
from controllers.chat_controller import chat_router

app = FastAPI(title="VS Code Code Assistant")

app.include_router(chat_router, prefix="/chat")

@app.get("/")
def root():
    return {"message": "VS Code Code Assistant is running."}
