from utils.language_utils import infer_language

def extract_context(data: dict):
    file_path = data.get("file_path", "")
    full_content = data.get("full_content", "")
    code_before_cursor = data.get("code_before_cursor", "")
    code_after_cursor = data.get("code_after_cursor", "")
    codebase_context = data.get("codebase_context", "")
    user_instruction = data.get("user_instruction", "")
    language = infer_language(file_path, full_content)
    return {
        "file_path": file_path,
        "full_content": full_content,
        "code_before_cursor": code_before_cursor,
        "code_after_cursor": code_after_cursor,
        "codebase_context": codebase_context,
        "user_instruction": user_instruction,
        "language": language,
    }
