from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from controllers.mode_router import handle_mode

chat_router = APIRouter()

@chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            response = await handle_mode(data)
            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass
