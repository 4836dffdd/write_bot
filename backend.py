# backend.py
import logging  # <--- [新增] 用于调用 logging.info
import logger   # <--- [新增] 引入配置模块，确保日志生效
from openai import OpenAI
from typing import Generator, List, Dict
import config

class AIWriter:
    """
    AI 核心逻辑类
    负责与 LLM 进行通信，不处理任何 UI 逻辑。
    """

    def __init__(self):
        # <--- [新增] 记录初始化动作
        logging.info("正在初始化 AIWriter Client...")
        self.client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)

    def generate_stream(
        self, messages: List[Dict[str, str]], temperature: float, max_tokens: int
    ) -> Generator[str, None, None]:
        """
        生成流式回复
        """
        # <--- [新增] 记录每次调用的参数，方便后续分析用户喜欢什么样的参数
        logging.info(f"开始生成任务: temp={temperature}, tokens={max_tokens}, msg_count={len(messages)}")
        
        try:
            stream = self.client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True, 
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            # <--- [新增] 可以在这里记录生成完成（可选）
            # logging.info("生成任务完成")

        except Exception as e:
            # <--- [新增] 关键！记录报错堆栈，以后 VPS 只要红了就看这里
            logging.error(f"AI 连接或生成失败: {str(e)}")
            yield f"\n[系统错误] AI 连接失败: {str(e)}"