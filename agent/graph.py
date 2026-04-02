from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from .tools import tools
from .prompt import SYSTEM_PROMPT

def create_financial_agent():
    llm = ChatOpenAI(model="gpt-4-0613", temperature=0.1)
    
    memory = MemorySaver()
    
    agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=SYSTEM_PROMPT
    )
    return agent