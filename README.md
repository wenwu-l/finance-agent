# Finance Agent - 金融分析 Agent

**基于 LangGraph + LangChain 的 Agent 金融分析系统**

一个功能强大的金融分析智能 Agent，能够自动获取股票实时数据、进行基本面分析、技术面分析、新闻情绪分析，并给出客观的投资参考建议。

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-FF6F00?style=for-the-badge)

## ✨ 项目构建

- **多 Agent 架构**：使用 LangGraph 构建，支持 Planner、Tool Calling、Memory 等进阶特性
- **实时数据获取**：集成股票 API（支持港股、美股等）
- **全面分析能力**：
  - 实时股价与行情
  - 基本面分析（财务状况、估值等）
  - 技术面分析（K线指标、趋势）
  - 新闻情绪分析
- **对话记忆**：支持多轮对话，记住上下文
- **易于扩展**：模块化设计，方便添加新工具和 Agent

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/wenwu-l/finance-agent.git
cd finance-agent
