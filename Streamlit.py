import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.language_models.llms import LLM
import tiktoken
import streamlit as st

from src.summarize.summarization import sumarize

st.set_page_config(page_title="Text Summarization app")
st.title("Summarization Tool")
url_link=st.text_area(label="Past URL or Type text",placeholder="Give your content")


with st.form('Summarize form',clear_on_submit=True):
    submit=st.form_submit_button('Submit')
    if submit:
        with st.spinner("Generating"):
            try:
                text=sumarize(url_link)
                st.info(text)
            except ValueError:
                st.info("The Web Page content is too much to summarize.")