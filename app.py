# app.py
import streamlit as st
import config
from backend import AIWriter

# --- 1. 页面基础设置 (读取 Config) ---
st.set_page_config(
    page_title=config.PAGE_TITLE, page_icon=config.PAGE_ICON, layout=config.LAYOUT_STYLE
)


# --- 2. 初始化核心引擎 (单例模式) ---
# 使用 cache_resource 确保 AIWriter 只被初始化一次，不用每次刷新都重连
@st.cache_resource
def get_writer():
    return AIWriter()


writer = get_writer()

# --- 3. 侧边栏：可变量调节区 (Variables) ---
with st.sidebar:
    st.header("🎛️ 写作控制台")

    # 变量 1: 系统人设 (可实时修改)
    system_prompt_input = st.text_area(
        "🧠 系统人设 (System Prompt)",
        value=config.DEFAULT_SYSTEM_PROMPT,
        height=200,
        help="在这里定义 AI 的身份和行为准则",
    )

    st.markdown("---")

    # 变量 2: 模型参数
    temperature = st.slider(
        "🌡️ 思维发散度 (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=config.DEFAULT_TEMP,
        step=0.1,
    )

    max_tokens = st.number_input(
        "📏 最大篇幅 (Tokens)",
        min_value=100,
        max_value=8000,
        value=config.DEFAULT_MAX_TOKENS,
        step=100,
    )

    # 功能按钮
    if st.button("🗑️ 清空对话历史", type="primary"):
        st.session_state.messages = []
        st.rerun()

# --- 4. 主界面逻辑 ---
st.title(config.PAGE_TITLE)

# 初始化 Session State (记忆存储)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    # 不显示 system prompt，只显示 user 和 assistant
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 5. 处理用户交互 ---
if user_input := st.chat_input("请输入写作指令..."):
    # A. 显示用户输入
    with st.chat_message("user"):
        st.markdown(user_input)

    # B. 构造请求消息列表
    # 技巧：每次发送时，动态把侧边栏的 System Prompt 插到第一条
    # 这样用户在侧边栏改了人设，下一句对话立刻生效
    full_messages = [{"role": "system", "content": system_prompt_input}]
    # 追加历史记录（排除旧的 system prompt，防止重复）
    full_messages.extend(
        [m for m in st.session_state.messages if m["role"] != "system"]
    )
    # 追加当前输入
    full_messages.append({"role": "user", "content": user_input})

    # C. 调用后端生成
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # 调用逻辑层
        stream_generator = writer.generate_stream(
            messages=full_messages, temperature=temperature, max_tokens=max_tokens
        )

        # 实时渲染
        for chunk in stream_generator:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    # D. 记入历史 (注意：我们只存 user 和 assistant，不存 system，system 每次动态取)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": full_response})
