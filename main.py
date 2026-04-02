from dotenv import load_dotenv
load_dotenv()

from agent.graph import create_financial_agent

# 创建 Agent
agent = create_financial_agent("gpt-4-0613", tools=tools)

# 会话配置（记忆用）
config = {"configurable": {"thread_id": "finance_001"}}

# 测试查询（你可以之后改成其他股票）
query = "请全面分析台积电（2330.TW），包括当前价格、财务状况、技术指标、最新新闻，并给出客观的投资参考建议"

response = agent.invoke(
    {"messages": [{"role": "user", "content": query}]},
    config=config
)

print("\n=== 台积电金融分析报告 ===\n")
print(response["messages"][-1].content)