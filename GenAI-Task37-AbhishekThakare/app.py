"""
app.py

Streamlit UI on top of the AstraDB RAG pipeline in astra_rag.py.
st.session_state holds the built chain and the conversation history.

Run with:  streamlit run app.py
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from astra_rag import get_embeddings, get_astra_vectorstore, load_and_split_pdf, build_rag_chain

st.set_page_config(page_title="AstraDB PDF RAG", page_icon="📄")
st.title("📄 AstraDB PDF Query RAG")
st.caption("Ask questions about the uploaded PDF - answered from AstraDB-stored embeddings.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "setup_error" not in st.session_state:
    st.session_state.setup_error = None

DEFAULT_PDF = "data/Employee_Handbook.pdf"

with st.sidebar:
    st.header("Setup")
    st.caption("Requires ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_API_ENDPOINT in your .env file.")

    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])
    use_default = st.checkbox("Use the default Employee Handbook instead", value=not uploaded_pdf)

    if st.button("Load PDF into AstraDB"):
        pdf_path = None
        if uploaded_pdf:
            pdf_path = f"/tmp/{uploaded_pdf.name}"
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())
        elif use_default:
            pdf_path = DEFAULT_PDF

        if not pdf_path:
            st.warning("Upload a PDF or check the default-handbook box first.")
        else:
            with st.spinner("Loading, splitting, embedding, and storing in AstraDB..."):
                try:
                    chunks = load_and_split_pdf(pdf_path)
                    embeddings = get_embeddings()
                    vectorstore = get_astra_vectorstore(embeddings)
                    vectorstore.add_documents(chunks)
                    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                    st.session_state.rag_chain = build_rag_chain(retriever)
                    st.session_state.chat_history = []
                    st.session_state.setup_error = None
                    st.success(f"Loaded {len(chunks)} chunks into AstraDB.")
                except Exception as e:
                    st.session_state.setup_error = str(e)
                    st.session_state.rag_chain = None

    if st.session_state.setup_error:
        st.error(f"Setup failed: {st.session_state.setup_error}")

for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

question = st.chat_input("Ask a question about the PDF...")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    if st.session_state.rag_chain is None:
        answer = (
            "No PDF is loaded into AstraDB yet - use the sidebar to load one first. "
            "If setup failed above, check that your AstraDB credentials and internet "
            "connection are both working."
        )
    else:
        try:
            answer = st.session_state.rag_chain.invoke(
                {"question": question, "chat_history": st.session_state.chat_history}
            )
        except Exception as e:
            answer = f"Something went wrong answering that: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.chat_history.append(HumanMessage(content=question))
    st.session_state.chat_history.append(AIMessage(content=answer))
