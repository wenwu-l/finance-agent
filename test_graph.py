import pytest
from unittest.mock import patch, MagicMock


class TestCreateFinancialAgent:
    """测试 create_financial_agent 函数"""

    def test_create_financial_agent_success(self):
        """测试成功创建金融代理的情况"""
        # 创建所有需要的模拟对象
        mock_chat_openai = MagicMock()
        mock_memory_saver = MagicMock()
        mock_create_agent = MagicMock()
        mock_llm = MagicMock()
        mock_memory = MagicMock()
        mock_agent = MagicMock()
        
        # 设置返回值
        mock_chat_openai.return_value = mock_llm
        mock_memory_saver.return_value = mock_memory
        mock_create_agent.return_value = mock_agent
        
        # 全局打补丁，mock 所有依赖
        with patch.dict('sys.modules', {
            'langchain_openai': MagicMock(ChatOpenAI=mock_chat_openai),
            'langchain.agents': MagicMock(create_agent=mock_create_agent),
            'langgraph.checkpoint.memory': MagicMock(MemorySaver=mock_memory_saver)
        }):
            # 现在可以安全导入并测试
            from agent.graph import create_financial_agent
            
            # 调用函数
            result = create_financial_agent()
            
            # 验证 ChatOpenAI 被正确调用
            mock_chat_openai.assert_called_once_with(
                model="gpt-4-0613",
                temperature=0.1
            )
            
            # 验证 MemorySaver 被调用
            mock_memory_saver.assert_called_once()
            
            # 验证返回结果
            assert result == mock_agent
            assert result is not None

    def test_create_financial_agent_llm_parameters(self):
        """测试 LLM 参数配置是否正确"""
        mock_chat_openai = MagicMock()
        mock_memory_saver = MagicMock()
        mock_create_agent = MagicMock()
        mock_llm = MagicMock()
        mock_memory = MagicMock()
        mock_agent = MagicMock()
        
        mock_chat_openai.return_value = mock_llm
        mock_memory_saver.return_value = mock_memory
        mock_create_agent.return_value = mock_agent
        
        with patch.dict('sys.modules', {
            'langchain_openai': MagicMock(ChatOpenAI=mock_chat_openai),
            'langchain.agents': MagicMock(create_agent=mock_create_agent),
            'langgraph.checkpoint.memory': MagicMock(MemorySaver=mock_memory_saver)
        }):
            from agent.graph import create_financial_agent
            
            # 调用函数
            create_financial_agent()
            
            # 验证模型参数
            mock_chat_openai.assert_called_once()
            call_args = mock_chat_openai.call_args
            assert call_args[1]['model'] == "gpt-4-0613"
            assert call_args[1]['temperature'] == 0.1

    def test_create_financial_agent_memory_initialization(self):
        """测试内存保存器初始化"""
        mock_chat_openai = MagicMock()
        mock_memory_saver = MagicMock()
        mock_create_agent = MagicMock()
        mock_llm = MagicMock()
        mock_memory = MagicMock()
        mock_agent = MagicMock()
        
        mock_chat_openai.return_value = mock_llm
        mock_memory_saver.return_value = mock_memory
        mock_create_agent.return_value = mock_agent
        
        with patch.dict('sys.modules', {
            'langchain_openai': MagicMock(ChatOpenAI=mock_chat_openai),
            'langchain.agents': MagicMock(create_agent=mock_create_agent),
            'langgraph.checkpoint.memory': MagicMock(MemorySaver=mock_memory_saver)
        }):
            from agent.graph import create_financial_agent
            
            # 调用函数
            create_financial_agent()
            
            # 验证 MemorySaver 被调用且只调用一次
            mock_memory_saver.assert_called_once()

    def test_create_financial_agent_agent_configuration(self):
        """测试代理配置参数"""
        mock_chat_openai = MagicMock()
        mock_memory_saver = MagicMock()
        mock_create_agent = MagicMock()
        mock_llm = MagicMock()
        mock_memory = MagicMock()
        mock_agent = MagicMock()
        
        mock_chat_openai.return_value = mock_llm
        mock_memory_saver.return_value = mock_memory
        mock_create_agent.return_value = mock_agent
        
        with patch.dict('sys.modules', {
            'langchain_openai': MagicMock(ChatOpenAI=mock_chat_openai),
            'langchain.agents': MagicMock(create_agent=mock_create_agent),
            'langgraph.checkpoint.memory': MagicMock(MemorySaver=mock_memory_saver)
        }):
            from agent.graph import create_financial_agent
            
            # 调用函数
            result = create_financial_agent()
            
            # 验证 create_agent 的调用参数
            assert mock_create_agent.call_count == 1
            call_kwargs = mock_create_agent.call_args[1]
            
            # 验证所有必需参数都存在
            assert 'model' in call_kwargs
            assert 'tools' in call_kwargs
            assert 'checkpointer' in call_kwargs
            assert 'state_modifier' in call_kwargs
            
            # 验证参数值
            assert call_kwargs['model'] == mock_llm
            assert call_kwargs['checkpointer'] == mock_memory
