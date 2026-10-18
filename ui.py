import streamlit as st
import httpx

# Your live Render API URL
API_URL = "https://ai-journey-api.onrender.com"

st.set_page_config(page_title="AI Document Assistant", page_icon="📄")
st.title("📄 AI Document Assistant")
st.caption("Upload a document and ask questions about it.")

# Sidebar for document upload
with st.sidebar:
    st.header("1. Upload Document")
    doc_id = st.text_input("Document ID", value="test01")
    text_input = st.text_area("Paste your document text here", height=300)
    
    if st.button("Upload & Process"):
        if text_input.strip():
            with st.spinner("Chunking and embedding..."):
                try:
                    response = httpx.post(
                        f"{API_URL}/documents/upload",
                        json={"doc_id": doc_id, "text": text_input},
                        timeout=60.0
                    )
                    if response.status_code == 200:
                        st.success("Document processed successfully!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect: {e}")
        else:
            st.warning("Please paste some text first.")

# Main chat area
st.header("2. Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    st.info(f"**Source {i+1}:** {source}")

if prompt := st.chat_input("Ask a question about the document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = httpx.post(
                    f"{API_URL}/documents/ask",
                    json={"doc_id": doc_id, "question": prompt},
                    timeout=60.0
                )
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["answer"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"],
                        "sources": data["sources"]
                    })
                    with st.expander("View Sources"):
                        for i, source in enumerate(data["sources"]):
                            st.info(f"**Source {i+1}:** {source}")
                else:
                    st.error("The API returned an error.")
            except Exception as e:
                st.error(f"Connection failed: {e}")