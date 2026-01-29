# backend.py
from openai import OpenAI
from typing import Generator, List, Dict
import config  # 导入配置

class AIWriter:
    """
    AI 核心逻辑类
    负责与 LLM 进行通信，不处理任何 UI 逻辑。
    """
    def __init__(self):
        # 初始化客户端 (只做一次)
        self.client = OpenAI(
            api_key=config.API_KEY,
            base_url=config.BASE_URL
        )

    def generate_stream(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float, 
        max_tokens: int
    ) -> Generator[str, None, None]:
        """
        生成流式回复
        :param messages: 完整的对话历史 [{"role": "user", "content": "..."}]
        :param temperature: 活跃度 (UI 传进来的)
        :param max_tokens: 最大长度 (UI 传进来的)
        :return: 生成器，每次吐出一个字符片段
        """
        try:
            stream = self.client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,  # 强制开启流式
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"\n[系统错误] AI 连接失败: {str(e)}"