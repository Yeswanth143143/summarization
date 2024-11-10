import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.language_models.llms import LLM
import tiktoken
from urllib.parse import urlparse

api_key=os.getenv("OPENAI_KEY")


def check_url(url):
    try:
        result=urlparse(url)
        return result.scheme in ["http","https"] and bool(result.netloc)
    except:
        return False
    
def loader(url):
    loader=WebBaseLoader(url)
    docs=loader.load()
    return docs

def token_length(text: str) -> int:
    encoding=tiktoken.get_encoding(encoding_name="cl100k_base")
    len_tokens=len(encoding.encode(text))
    return len_tokens

def sumarize(input):
    context_length= 5000
    llm=ChatOpenAI(api_key=api_key,model="gpt-3.5-turbo")
    if check_url(input):  
        prompt=ChatPromptTemplate.from_messages([('system','you are an expert in Summarization. Summarize the content in brackets {context}')])
        chain=create_stuff_documents_chain(llm,prompt)
        # Retrive the document from URL
        docs_obj=loader(input)
        # Check the Number of the tokens
        tokens=token_length(docs_obj[0].page_content)
        if tokens < context_length:
            summarized=chain.invoke({"context":docs_obj})
        else: 
            raise ValueError("Content is beyond the limit.")
    else:
        prompt=ChatPromptTemplate.from_messages([('system','you are an expert in Summarization. Summarize the following content:'),('user','{input}')])
        chain= prompt | llm
        tokens=token_length(input)
        if tokens < context_length:
            summarized=chain.invoke(input).content
        else:
            raise ValueError("Content is beyond the limit.")
    return summarized