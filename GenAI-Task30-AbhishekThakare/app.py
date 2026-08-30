"""
app.py

Task 7 & 8: the Streamlit chat interface, wired up to the RAG backend in
rag_groq.py. Run with:

    streamlit run app.py

Sidebar lets you upload a PDF/text file (or just use the default onboarding
notes that ship with this project), then the main area is a normal chat
interface on top of whatever got loaded.
"""

import os
import tempfile

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from rag_groq import build_retriever, build_rag_chain

st.set_page_config(page_title="Chat Groq RAG", page_icon="⚡")
st.title("⚡ Chat Groq RAG Application")
st.caption("Fast, grounded document Q&A powered by Groq + LangChain")

# --- session state (Task 7: session state to store chat history) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "doc_names" not in st.session_state:
    st.session_state.doc_names = []

DEFAULT_PATHS = ["data/notes.txt", "data/policies.txt"]

# --- sidebar: file uploader + knowledge base build (Task 7) ---
with st.sidebar:
    st.header("Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or text file(s)", type=["pdf", "txt"], accept_multiple_files=True
    )
    use_default = st.checkbox(
        "Use the default onboarding notes instead", value=not uploaded_files
    )
    build_clicked = st.button("Build / rebuild knowledge base")

    if build_clicked:
        paths = []
        if uploaded_files:
            tmp_dir = tempfile.mkdtemp()
            for f in uploaded_files:
                path = os.path.join(tmp_dir, f.name)
                with open(path, "wb") as out_file:
                    out_file.write(f.getbuffer())
                paths.append(path)
        elif use_default:
            paths = [p for p in DEFAULT_PATHS if os.path.exists(p)]

        if not paths:
            st.warning("Upload a file, or check the default-notes box, then try again.")
        else:
            with st.spinner("Loading, splitting, and embedding documents..."):
                try:
                    retriever = build_retriever(paths)
                    st.session_state.rag_chain = build_rag_chain(retriever)
                    st.session_state.doc_names = [os.path.basename(p) for p in paths]
                    st.session_state.chat_history = []
                    st.success(f"Ready. Loaded: {', '.join(st.session_state.doc_names)}")
                except Exception as e:
                    st.error(f"Couldn't build the knowledge base: {e}")

    if st.session_state.doc_names:
        st.caption("Currently loaded: " + ", ".join(st.session_state.doc_names))
    else:
        st.caption("No documents loaded yet.")

# --- chat message display (Task 7) ---
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# --- chat input + backend integration (Task 8) ---
user_question = st.chat_input("Ask a question about the loaded documents...")

if user_question:
    with st.chat_message("user"):
        st.markdown(user_question)

    if st.session_state.rag_chain is None:
        answer = (
            "No knowledge base is loaded yet - upload a file or check the "
            "default-notes box in the sidebar, then click 'Build / rebuild "
            "knowledge base' before asking a question."
        )
    else:
        try:
            answer = st.session_state.rag_chain.invoke(
                {"question": user_question, "chat_history": st.session_state.chat_history}
            )
        except Exception as e:
            # Task 8: handle errors gracefully instead of the whole app crashing
            answer = f"Something went wrong talking to Groq: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append(HumanMessage(content=user_question))
    st.session_state.chat_history.append(AIMessage(content=answer))
