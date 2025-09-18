from chains.ask_chain import get_ask_chain
from tools.context_extractor import extract_context

def format_chat_history(chat_history):
    if not chat_history:
        return ""
    return "\n".join(
        f"{item['role'].capitalize()}: {item['content']}" for item in chat_history
    )

async def handle_ask(data: dict):
    context = extract_context(data)
    chat_history = data.get("chat_history", [])
    context["chat_history"] = format_chat_history(chat_history)
    chain = get_ask_chain()
    result = await chain.acall(context)
    return {"result": result["output"]}