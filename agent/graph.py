import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from .tools import tools
from .prompt import SYSTEM_PROMPT

def create_financial_agent():
    """使用 DeepSeek 模型 - 最稳定写法"""
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not deepseek_key or not deepseek_key.startswith("sk-"):
        raise ValueError("DEEPSEEK_API_KEY 未正确加载或格式错误！请检查 .env 文件")
    
    print(f"正在使用 DeepSeek Key: {deepseek_key[:15]}...")  # 打印前15位用于调试
    
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=deepseek_key,
        base_url="https://api.deepseek.com",   # 推荐不加 /v1
        temperature=0.1,
        max_tokens=8192,
        # 添加以下参数提高稳定性
        openai_api_base="https://api.deepseek.com",
    )
    
    memory = MemorySaver()
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        prompt=SYSTEM_PROMPT
    )
    return agent