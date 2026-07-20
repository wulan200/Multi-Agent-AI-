import streamlit as st
import time

from supervisor import supervisor_agent

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HR Recruitment AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SESSION
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

[data-testid="stAppViewContainer"]{
background:#212121;
}

[data-testid="stSidebar"]{
background:#171717;
border-right:1px solid #333;
}

[data-testid="stChatMessage"]{
padding-top:18px;
padding-bottom:18px;
}

[data-testid="stChatInput"]{
position:fixed;
bottom:20px;
left:310px;
right:30px;
background:#212121;
padding-top:15px;
}

.block-container{

padding-top:30px;
padding-bottom:120px;
max-width:900px;

}

.title{

font-size:42px;

font-weight:700;

text-align:center;

color:white;

margin-top:70px;

}

.subtitle{

text-align:center;

color:#A1A1AA;

font-size:18px;

margin-bottom:60px;

}

.agent{

display:inline-block;

padding:6px 12px;

border-radius:20px;

background:#7C3AED;

color:white;

font-size:13px;

margin-bottom:12px;

}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 HR Recruitment AI")

    st.caption("Multi-Agent System")

    st.button("➕ New Chat", use_container_width=True)

    st.divider()

    st.subheader("History")

    if len(st.session_state.messages)==0:

        st.caption("Belum ada percakapan")

    else:

        st.write("💬 Recruitment Discussion")

    st.divider()

    st.subheader("Knowledge Base")

    st.success("10 PDF Loaded")

    st.divider()

    st.subheader("Powered By")

    st.caption("✅ LangChain")

    st.caption("✅ FAISS")

    st.caption("✅ Groq")

# ==========================================
# WELCOME
# ==========================================

if len(st.session_state.messages)==0:

    st.markdown("""

<div class="title">

🤖 HR Recruitment AI

</div>

<div class="subtitle">

How can I help you with recruitment today?

</div>

""",unsafe_allow_html=True)