"""
Campus FAQ Assistant — An AI chatbot that answers university admissions
and campus life questions for prospective and current students.

Built with Streamlit + OpenAI / Anthropic APIs.
"""

import time
import streamlit as st

from llm_client import get_llm_response, AVAILABLE_PROVIDERS
from system_prompt import SYSTEM_PROMPT

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Campus FAQ Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

MAX_HISTORY_TURNS = 12  # number of (user, assistant) turn-pairs kept in context


# ----------------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------------
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []  # list of {"role": ..., "content": ...}
    if "provider" not in st.session_state:
        st.session_state.provider = "Anthropic (Claude)"
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""


init_session_state()


# ----------------------------------------------------------------------------
# Sidebar — settings, provider/model selection, clear/reset
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎓 Campus FAQ Assistant")
    st.caption("Your AI guide for admissions, courses, fees, and campus life questions.")

    st.divider()

    st.subheader("⚙️ Settings")

    provider = st.selectbox(
        "Choose LLM Provider",
        options=list(AVAILABLE_PROVIDERS.keys()),
        index=list(AVAILABLE_PROVIDERS.keys()).index(st.session_state.provider),
        help="Pick which API powers the chatbot.",
    )
    st.session_state.provider = provider

    model_options = AVAILABLE_PROVIDERS[provider]["models"]
    model = st.selectbox("Model", options=model_options, index=0)

    api_key_input = st.text_input(
        f"{provider} API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-... or your key",
        help="Your key is used only for this session and is never stored or logged.",
    )
    st.session_state.api_key = api_key_input

    # Optional fallback: if the deployer set a key via Streamlit Secrets
    # (Settings -> Secrets on Streamlit Cloud), use it when the visitor
    # hasn't typed one in. This lets a demo deployment work out-of-the-box
    # without exposing the key in the repo. See README "Deploy" section.
    if not st.session_state.api_key:
        secret_key_name = (
            "ANTHROPIC_API_KEY" if provider == "Anthropic (Claude)" else "OPENAI_API_KEY"
        )
        st.session_state.api_key = st.secrets.get(secret_key_name, "")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.messages = []
            st.session_state.api_key = ""
            st.rerun()

    st.divider()
    st.caption(
        "💡 **Tip:** This bot specializes in university admissions and campus "
        "FAQs — eligibility, courses, fees, scholarships, hostel life, and "
        "contact info. Ask it anything in that space!"
    )

    with st.expander("ℹ️ About this project"):
        st.markdown(
            """
**Tools & Tech:** Python, Streamlit, OpenAI / Anthropic APIs

**Core features:**
- Multi-turn conversation with context memory
- Topic-focused system prompt (university admissions & campus FAQ)
- Conversation history management
- Clear / Reset functionality
- Typing indicator while the model responds
            """
        )


# ----------------------------------------------------------------------------
# Main chat area
# ----------------------------------------------------------------------------
st.title("🎓 Campus FAQ Assistant")
st.caption(
    "Ask me about admissions eligibility, courses offered, fees & scholarships, "
    "hostel life, or how to reach the right department."
)

# Render existing conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Empty-state welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Hi! 👋 I'm the **Campus FAQ Assistant**. I can help with:\n\n"
            "- 📋 Admissions eligibility & application process\n"
            "- 🎓 Courses & programs offered\n"
            "- 💰 Fees & scholarships\n"
            "- 🏠 Hostel & campus life\n"
            "- 📞 Contact info for departments\n\n"
            "What would you like to know?"
        )

# ----------------------------------------------------------------------------
# Chat input & response generation
# ----------------------------------------------------------------------------
user_input = st.chat_input("Ask about admissions, courses, fees, hostel life...")

if user_input:
    if not st.session_state.api_key:
        st.error(
            f"⚠️ Please enter your {st.session_state.provider} API key in the "
            "sidebar to start chatting."
        )
    else:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Trim history to last N turns to keep context manageable
        trimmed_history = st.session_state.messages[-(MAX_HISTORY_TURNS * 2):]

        # Generate assistant response with a typing indicator
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("▌ _typing..._")
            try:
                response_text = get_llm_response(
                    provider=st.session_state.provider,
                    model=model,
                    api_key=st.session_state.api_key,
                    system_prompt=SYSTEM_PROMPT,
                    history=trimmed_history,
                )
            except Exception as e:
                response_text = (
                    f"⚠️ Something went wrong calling the {st.session_state.provider} "
                    f"API: `{e}`\n\nPlease check your API key and try again."
                )

            # Simple streaming-style reveal for a nicer feel
            displayed = ""
            for chunk in response_text.split(" "):
                displayed += chunk + " "
                placeholder.markdown(displayed + "▌")
                time.sleep(0.01)
            placeholder.markdown(displayed.strip())

        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )
