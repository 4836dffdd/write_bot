import os
from dotenv import load_dotenv

# 加载 .env 文件到系统环境变量
load_dotenv()

# 读取变量
api_key = os.getenv("SILICONFLOW_API_KEY")
base_url = os.getenv("SILICONFLOW_BASE_URL")