# app.py
import streamlit as st
import config

# --- 1. 页面基础设置 (必须是第一个 Streamlit 命令) ---
st.set_page_config(
    page_title=config.PAGE_TITLE, page_icon=config.PAGE_ICON, layout=config.LAYOUT_STYLE
)

import logging  # <--- [新增]
import logger  # <--- [新增] 确保日志系统就绪
from backend import AIWriter


# --- 2. 初始化核心引擎 ---
@st.cache_resource
def get_writer():
    # <--- [新增] 记录缓存命中情况
    logging.info("实例化新的 AIWriter (Cache Miss)")
    return AIWriter()


writer = get_writer()

# --- 3. 侧边栏 ---
with st.sidebar:
    st.header("🎛️ 写作控制台")
    system_prompt_input = st.text_area(
        "🧠 系统人设 (System Prompt)",
        value=config.DEFAULT_SYSTEM_PROMPT,
        height=200,
    )
    st.markdown("---")
    temperature = st.slider("🌡️ 思维发散度", 0.0, 1.0, config.DEFAULT_TEMP, 0.1)
    max_tokens = st.number_input(
        "📏 最大篇幅", 100, 8000, config.DEFAULT_MAX_TOKENS, 100
    )

    if st.button("🗑️ 清空对话历史", type="primary"):
        logging.info("用户点击了清空历史")  # <--- [新增] 埋点
        st.session_state.messages = []
        st.rerun()

# --- 4. 主界面逻辑 ---
st.title(config.PAGE_TITLE)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 5. 处理用户交互 ---
if user_input := st.chat_input("请输入写作指令..."):
    # <--- [新增] 记录用户活跃动作
    logging.info("用户提交了新的写作指令")

    # 显示用户输入
    with st.chat_message("user"):
        st.markdown(user_input)

    # 构造请求
    full_messages = [{"role": "system", "content": system_prompt_input}]
    full_messages.extend(
        [m for m in st.session_state.messages if m["role"] != "system"]
    )
    full_messages.append({"role": "user", "content": user_input})

    # 调用后端
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        stream_generator = writer.generate_stream(
            messages=full_messages, temperature=temperature, max_tokens=max_tokens
        )

        for chunk in stream_generator:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    # 记入历史
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": full_response})
