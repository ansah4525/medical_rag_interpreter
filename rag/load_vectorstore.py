from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def load_vectorstore():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    return Chroma(
        persist_directory="vector_db/chroma_lab_db",
        embedding_function=embeddings,
        collection_name="lab_knowledge"
    )
