import json
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from chunker import chunk_lab_json

load_dotenv()

with open("data/medical_reference_knowledge.json") as f:
    medical_json = json.load(f)

docs = chunk_lab_json(medical_json)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="vector_db/chroma_lab_db",
    collection_name="lab_knowledge"
)

db.persist()
print("✅ Vector database created successfully.")
