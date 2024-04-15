import bs4 # for Scrapping
import os # to im
from dotenv import load_dotenv 
import google.generativeai as genai 
from langchain_google_genai import ChatGoogleGenerativeAI #Google genai chat models
from langchain_community.document_loaders import WebBaseLoader # document loader
from langchain_community.vectorstores import Chroma # Vector store
from langchain_google_genai import GoogleGenerativeAIEmbeddings # embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter # splits
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
llm = ChatGoogleGenerativeAI(model= "gemini-pro") 

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/",
                       bs_kwargs = dict(
                           parse_only = bs4.SoupStrainer(
                               class_= ("post-content", "post-title","post-header")
                           )
                       ),
                    )
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000, chunk_overlap = 200)
splits = text_splitter.split_documents(docs)
embeddings = GoogleGenerativeAIEmbeddings(model = 'models/embedding-001')
vectorstore = Chroma.from_documents(documents = splits, embedding = embeddings)

retriever = vectorstore.as_retriever()

# this is to pull a already existing prompt
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context":retriever| format_docs, "question":RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("Please give me your prompt."))