from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_mistralai import MistralAIEmbeddings
def load_vectorstore():
    

    embeddings = MistralAIEmbeddings(
        model="mistral-embed"
    )

    return Chroma(
        persist_directory="vector_db/chroma_lab_db",
        embedding_function=embeddings,
        collection_name="lab_knowledge"
    )
