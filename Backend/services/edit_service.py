import re
from chains.edit_chain import get_edit_chain
from tools.context_extractor import extract_context

def clean_code_output(output: str) -> str:
    code = re.sub(r"^```[a-zA-Z]*\n?", "", output.strip())
    code = re.sub(r"\n?```$", "", code)
    return code.strip()

def format_chat_history(chat_history):
    if not chat_history:
        return ""
    return "\n".join(
        f"{item['role'].capitalize()}: {item['content']}" for item in chat_history
    )

async def handle_edit(data: dict):
    context = extract_context(data)
    chat_history = data.get("chat_history", [])
    context["chat_history"] = format_chat_history(chat_history)
    chain = get_edit_chain()
    result = await chain.acall(context)
    code = clean_code_output(result["output"])
    explanation = result.get("explanation", "Code updated in the tagged file.")
    return {"result": code, "explanation": explanation}