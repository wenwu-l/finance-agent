from dotenv import load_dotenv
import os
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

print(llm.invoke("你好，请说一句中文"))