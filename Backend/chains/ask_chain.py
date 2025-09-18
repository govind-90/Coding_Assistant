from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, MODEL_NAME

def get_ask_chain():
    prompt = PromptTemplate(
        input_variables=["chat_history", "user_instruction", "file_path", "language", "full_content", "codebase_context"],
        template=(
            "You are a code explanation assistant. "
            "Here is the previous conversation:\n"
            "{chat_history}\n"
            "Given the following:\n"
            "File Path: {file_path}\n"
            "Language/Framework: {language}\n"
            "Full File Content: {full_content}\n"
            "Codebase Context: {codebase_context}\n"
            "User Question: {user_instruction}\n"
            "Answer the question with reasoning and code examples if relevant."
        )
    )
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3,
        max_output_tokens=1024,
    )
    return LLMChain(prompt=prompt, llm=llm, output_key="output")