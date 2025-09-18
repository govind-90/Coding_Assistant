from services.edit_service import handle_edit
from services.ask_service import handle_ask

async def handle_mode(data: dict):
    mode = data.get("mode")
    if mode == "edit":
        return await handle_edit(data)
    elif mode == "ask":
        return await handle_ask(data)
    else:
        return {"error": "Invalid mode"}
