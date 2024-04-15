import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.vectorstores.milvus import Milvus
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap


load_dotenv()
host = os.getenv('HOST')
port = os.getenv('PORT')
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {
    "temperature": 0.9,
    "top_k": 2,
}
llm = ChatGoogleGenerativeAI(model = "gemini-pro", generation_config =generation_config)

output_parser = StrOutputParser()

loaders = CSVLoader(file_path= "/Volumes/Ajeet/LLM Projects/CSV-QnA/Test-Sheet1.csv", encoding= "utf-8")
data = loaders.load()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
database = Milvus(embeddings,connection_args={'host':host,'port':port},collection_name="CSV_READER")




prompt = """S
### Instruction ###
You are a Virtual Assistant for Muktinath Bikas Bank. When a user asks a question you have to answer him based on the context and make sure
to provide all the details.
Context is given in triple back ticks: ```{context}```
Question is given in double back ticks:  ``{question}``
If the question is out of context, do not provide the wrong answer just say I am sorry i can't answer to that question.
"""

template = ChatPromptTemplate.from_template(prompt)


chain = RunnableMap(
    {
        "context": lambda x:database.similarity_search(x['question'], k = 8),
        "question": lambda x:x['question']
    }
)|template|llm|output_parser

def result(query:str):
    result = chain.invoke({'question':query})
    return {"text":result}


if __name__ == "__main__":
    query = input("Input your query")
    response= result(query= query)
    print("Response:",response)
