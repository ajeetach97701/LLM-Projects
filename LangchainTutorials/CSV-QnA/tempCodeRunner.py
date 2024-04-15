from langchain.vectorstores.milvus import Milvus
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import CSVLoader
from dotenv import load_dotenv
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
host = os.getenv('HOST')
port = os.getenv('PORT')
# embeddings = HuggingFaceEmbeddings(embeddings="sentence-transformers/all-MiniLM-L6-v2")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

loaders = CSVLoader(file_path= "/Volumes/Ajeet/LLM Projects/CSV-QnA/Test-Sheet1.csv", encoding= "utf-8")
data = loaders.load()


database = Milvus.from_documents(data, embeddings,connection_args={'host':host,'port':port},collection_name='CSV_READER')