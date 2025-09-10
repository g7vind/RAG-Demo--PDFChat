import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_templates import css, bot_template, user_template
import asyncio
import os

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=api_key
    )
    vectorstore = Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings
    )
    # print(vectorstore._collection.count())  # Debugging line to check the number of documents
    return vectorstore


def get_conversation_chain(vectorstore, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0,
        google_api_key=api_key
    )
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload PDFs and process them first!")
        return
    
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    st.header("Chat with multiple PDFs :books:")

    # API Key input in sidebar
    with st.sidebar:
        st.subheader("Configuration")
        
        # Get API key from user
        api_key = st.text_input(
            "Enter your Google Gemini API Key:",
            type="password",
            value=st.session_state.api_key,
            help="You can get your API key from Google AI Studio"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            os.environ["GOOGLE_API_KEY"] = api_key
            st.success("API Key set successfully!")
        else:
            st.warning("Please enter your Google Gemini API Key to continue.")
        
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", 
            accept_multiple_files=True,
            disabled=not api_key  # Disable if no API key
        )
        
        if st.button("Process", disabled=not api_key or not pdf_docs):
            if not api_key:
                st.error("Please enter your API key first!")
            elif not pdf_docs:
                st.error("Please upload at least one PDF file!")
            else:
                with st.spinner("Processing"):
                    try:
                        raw_text = get_pdf_text(pdf_docs)
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks, api_key)
                        st.session_state.conversation = get_conversation_chain(
                            vectorstore, api_key)
                        st.success("Documents processed successfully!")
                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")

    # Main chat interface
    if st.session_state.api_key:
        user_question = st.text_input("Ask a question about your documents:")
        if user_question:
            handle_userinput(user_question)
    else:
        st.info("👈 Please enter your Google Gemini API Key in the sidebar to get started.")


if __name__ == '__main__':
    main()