from dotenv import load_dotenv
import os
load_dotenv()

from agent.graph import create_financial_agent

agent = create_financial_agent()

config = {"configurable": {"thread_id": "finance_001"}}

query = "请全面分析小米集团（1810.HK），包括当前价格、财务状况、技术指标、最新新闻，并给出客观的投资参考建议"

response = agent.invoke(
    {"messages": [{"role": "user", "content": query}]},
    config=config
)

print("\n=== 小米集团金融分析报告 ===\n")
print(response["messages"][-1].content)