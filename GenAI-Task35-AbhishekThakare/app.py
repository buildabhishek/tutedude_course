"""
app.py

Task 3: a simple Streamlit chat app on top of the Text-to-Math agent.
st.session_state holds the running conversation (both the message list fed
back into the agent for context, and the display history), so a follow-up
like "what if it were 20% instead?" has the previous problem to refer back
to.

Run with:  streamlit run app.py
"""

import streamlit as st

from math_agent import build_math_agent, ask_math_agent

st.set_page_config(page_title="Text-to-Math Agent", page_icon="🧮")
st.title("🧮 Text-to-Math Agent")
st.caption("Ask a word problem - arithmetic, percentages, or simple algebra.")

# --- session state: conversation history + the agent itself ---
if "display_history" not in st.session_state:
    st.session_state.display_history = []  # [(role, content), ...] for rendering
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []  # raw {"role", "content"} dicts fed to the agent
if "agent" not in st.session_state:
    try:
        st.session_state.agent = build_math_agent()
        st.session_state.agent_error = None
    except Exception as e:
        st.session_state.agent = None
        st.session_state.agent_error = str(e)

with st.sidebar:
    st.header("Session")
    st.caption(f"Questions asked this session: {len(st.session_state.display_history) // 2}")
    if st.button("Clear conversation"):
        st.session_state.display_history = []
        st.session_state.agent_messages = []
        st.rerun()

if st.session_state.agent_error:
    st.warning(f"Agent isn't available right now: {st.session_state.agent_error}")

# --- render existing conversation ---
for role, content in st.session_state.display_history:
    with st.chat_message(role):
        st.markdown(content)

# --- chat input ---
question = st.chat_input("Ask a math word problem...")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    if st.session_state.agent is None:
        answer = (
            "The agent isn't available right now (see the warning above) - "
            "this needs Ollama running locally with llama3.2 pulled."
        )
    else:
        try:
            answer = ask_math_agent(
                st.session_state.agent, question, history=st.session_state.agent_messages
            )
        except Exception as e:
            answer = f"Something went wrong solving that: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    # keep both the display history and the raw message list the agent sees
    st.session_state.display_history.append(("user", question))
    st.session_state.display_history.append(("assistant", answer))
    st.session_state.agent_messages.append({"role": "user", "content": question})
    st.session_state.agent_messages.append({"role": "assistant", "content": answer})
