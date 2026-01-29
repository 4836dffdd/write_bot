# config.py
import os
from dotenv import load_dotenv

# 1. 加载环境变量 (.env)
load_dotenv()

# --- [机密部分] ---
API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = os.getenv("SILICONFLOW_BASE_URL")
MODEL_NAME = "deepseek-ai/DeepSeek-V3"  # 或 R1

# --- [UI 静态配置] ---
PAGE_TITLE = "DeepSeek 专业写作台"
PAGE_ICON = "✍️"
LAYOUT_STYLE = "wide"

# --- [参数默认值 (Invariants)] ---
# 这些是滑块的“出厂设置”，用户可以在网页上调，但基准在这里
DEFAULT_SYSTEM_PROMPT = """你是一个专业的写作助手。
请遵循以下原则：
1. 逻辑清晰，结构严谨。
2. 语言简练，避免废话。
3. 如果是代码，请提供注释。
"""
DEFAULT_TEMP = 0.7
DEFAULT_MAX_TOKENS = 2000