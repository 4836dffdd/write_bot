import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载环境变量
load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY")
base_url = os.getenv("SILICONFLOW_BASE_URL")

# 2. 页面配置
st.set_page_config(page_title="我的 AI 写作助手", page_icon="✍️", layout="wide")

st.title("🤖 DeepSeek V3 - 写作助手")

# 3. 侧边栏：控制台
with st.sidebar:
    st.header("🎛️ 参数控制")
    temperature = st.slider("思维活跃度", 0.0, 1.5, 0.7, step=0.1)
    max_tokens = st.number_input("最大长度", 100, 4000, 2000)
    st.markdown("---")
    st.caption("已连接 RackNerd VPS")

# 4. 初始化聊天记录 (让 AI 拥有记忆)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 处理用户输入
if prompt := st.chat_input("输入你的想法..."):
    # 显示用户的话
    with st.chat_message("user"):
        st.markdown(prompt)
    # 记入历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 7. 调用 AI (核心逻辑)
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 流式输出 (像打字机一样一个个字蹦出来)
        stream = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # 记入历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})