from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, MODEL_NAME

def get_edit_chain():
    prompt = PromptTemplate(
        input_variables=[
            "chat_history",
            "user_instruction",
            "file_path",
            "language",
            "full_content",
            "code_before_cursor",
            "code_after_cursor",
            "codebase_context"
        ],
        template=(
            "You are a code editing assistant for a code editor. "
            "Here is the previous conversation:\n"
            "{chat_history}\n"
            "Given the following:\n"
            "File Path: {file_path}\n"
            "Language/Framework: {language}\n"
            "Full File Content: {full_content}\n"
            "Code Before Cursor: {code_before_cursor}\n"
            "Code After Cursor: {code_after_cursor}\n"
            "Codebase Context: {codebase_context}\n"
            "User Instruction: {user_instruction}\n"
            "Edit the code as per instruction and return ONLY the full updated file as raw code, with NO markdown, NO triple backticks, and NO extra comments or explanations."
        )
    )
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
        max_output_tokens=2048,
    )
    return LLMChain(prompt=prompt, llm=llm, output_key="output")
