import streamlit as st
from dotenv import load_dotenv
import os

from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

from utils.fetcher import get_transcript

# Load .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Smart YouTube Bot", page_icon="🎥")
st.title("🎬 Smart YouTube Video Summarizer")

url = st.text_input("📎 Paste a YouTube video URL:")

if url:
    try:
        with st.spinner("Fetching transcript..."):
            transcript = get_transcript(url)
        st.success("Transcript fetched!")

        # Split large text into chunks
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_text(transcript)

        # Convert to LangChain Documents
        documents = [Document(page_content=chunk) for chunk in chunks]

        # Load chain
        llm = OpenAI(openai_api_key=openai_api_key, temperature=0.5)
        chain = load_qa_chain(llm, chain_type="stuff")

        choice = st.radio("Choose:", ["📄 Summary", "❓ Ask a Question"])

        if choice == "📄 Summary":
            with st.spinner("Summarizing..."):
                response = chain.run(input_documents=documents, question="Give a detailed summary.")
                st.markdown("### 📝 Summary:")
                st.write(response)

        elif choice == "❓ Ask a Question":
            query = st.text_input("Ask your question:")
            if query:
                with st.spinner("Thinking..."):
                    response = chain.run(input_documents=documents, question=query)
                    st.markdown("### 💬 Answer:")
                    st.write(response)

    except Exception as e:
        st.error(f"❌ Something went wrong!\n\nError: {e}")
