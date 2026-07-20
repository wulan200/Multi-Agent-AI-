import streamlit as st
import time
from supervisor import supervisor_agent

# 1. PAGE CONFIG (Hanya boleh dipanggil sekali di paling atas)
st.set_page_config(
    page_title="HR Recruitment AI",
    page_icon="🤖",
    layout="wide"
)

# 2. SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. SIDEBAR
with st.sidebar:
    st.title("🤖 HR Recruitment AI")

    # Menggunakan st.session_state.clear() agar reset total saat ganti chat
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.divider()
    st.markdown("### 🤖 Agents")
    st.write("• Supervisor")
    st.write("• CV Screening")
    st.write("• Interview")
    st.write("• Training")
    st.write("• Client")
    st.write("• Reporting")

    st.divider()
    st.markdown("### 📚 Knowledge Base")
    st.success("10 PDF Loaded")

# 4. HEADER
st.title("🤖 HR Recruitment AI")
st.caption("Enterprise Multi-Agent Recruitment Assistant")

# 5. CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.caption(f"🤖 {msg['agent']}")

        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.write("📄", s)

            c1, c2 = st.columns(2)
            c1.metric("Agent", msg["agent"])
            c2.metric("Time", f"{msg['time']:.2f} sec")

# 6. INPUT & AGENT PROCESSING
prompt = st.chat_input("Ask HR Recruitment AI...", key="hr_chat_input")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status = st.status("Processing...", expanded=True)
        status.write("🤖 Supervisor memilih agent...")
        time.sleep(.4)

        status.write("📚 Searching knowledge base...")
        time.sleep(.4)

        status.write("🧠 Generating answer...")
        
        start = time.perf_counter()
        result = supervisor_agent(prompt)
        end = time.perf_counter()
        
        response = result["answer"]
        response_time = end - start

        status.update(label="Completed", state="complete")
        st.caption(f"🤖 {result['selected_agent'].upper()}")

        placeholder = st.empty()
        text = ""

        for word in response.split():
            text += word + " "
            placeholder.markdown(text + "▌")
            time.sleep(0.01)

        placeholder.markdown(text)

        sources = []
        seen = set()
        for doc in result["documents"]:
            src = f"{doc.metadata['source']} | Page {doc.metadata['page'] + 1}"
            if src not in seen:
                seen.add(src)
                sources.append(src)

        with st.expander("📚 Sources"):
            for s in sources:
                st.write("📄", s)

        c1, c2 = st.columns(2)
        c1.metric("Agent", result["selected_agent"].upper())
        c2.metric("Response", f"{response_time:.2f} sec")

    st.session_state.messages.append({
        "role": "assistant",
        "agent": result["selected_agent"].upper(),
        "content": response,
        "sources": sources,
        "time": response_time
    })
    st.rerun()

# 7. CUSTOM CSS (Dipindahkan ke paling bawah agar rapi)
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

html, body, [class*="css"]{
    font-family: "Segoe UI", sans-serif;
}
.stApp, [data-testid="stAppViewContainer"]{
    background:#F8FAFC;
}
section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#111827;
}
section[data-testid="stSidebar"] .stButton>button{
    width:100%;
    background:#2563EB;
    color:white;
    border:none;
    border-radius:12px;
    height:45px;
    font-weight:600;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:#1D4ED8;
}
[data-testid="stChatMessage"]{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:20px;
    margin-bottom:20px;
    box-shadow:0 5px 15px rgba(0,0,0,.05);
}
[data-testid="stChatInput"]{
    background:white;
    border-top:1px solid #E5E7EB;
    padding-top:12px;
}
.stButton>button{
    border-radius:12px;
}
div[data-testid="metric-container"]{
    background:white;
    border:1px solid #E5E7EB;
    padding:15px;
    border-radius:14px;
    box-shadow:0 4px 10px rgba(0,0,0,.05);
}
.streamlit-expanderHeader{
    font-weight:bold;
}
h1, h2, h3{ color:#111827; }
p{ color:#374151; }
.stAlert{ border-radius:12px; }
::-webkit-scrollbar{ width:8px; }
::-webkit-scrollbar-thumb{ background:#CBD5E1; border-radius:10px; }
::-webkit-scrollbar-thumb:hover{ background:#94A3B8; }
.agent-badge{
    display:inline-block;
    padding:6px 12px;
    background:#2563EB;
    color:white;
    border-radius:30px;
    font-size:13px;
    font-weight:600;
    margin-bottom:10px;
}
.source-card{
    background:#F8FAFC;
    padding:12px;
    border-radius:12px;
    border:1px solid #E5E7EB;
    margin-bottom:10px;
}
[data-testid="stChatMessage"]{
    animation:fade .35s ease;
}
@keyframes fade{
    from{ opacity:0; transform:translateY(10px); }
    to{ opacity:1; transform:translateY(0px); }
}
.block-container{
    max-width:1000px;
    padding-top:30px;
    padding-bottom:120px;
}
</style>
""", unsafe_allow_html=True)
