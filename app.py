import os
from dotenv import load_dotenv

# 加载 .env 文件到系统环境变量
load_dotenv()

# 读取变量
api_key = os.getenv("SILICONFLOW_API_KEY")
base_url = os.getenv("SILICONFLOW_BASE_URL")

import streamlit as st
# ... 你的环境变量读取代码 ...

st.title("服务已连通")
st.write("如果看到这句话，说明 .env 和网络都通了！")