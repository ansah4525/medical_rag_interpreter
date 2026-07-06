
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.chains import RetrievalQA
from rag.load_vectorstore import load_vectorstore
from rag.prompt import get_prompt
from langchain_community.embeddings import HuggingFaceEmbeddings


# Load env vars (OPENAI_API_KEY)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
from langchain_mistralai import ChatMistralAI

print("Tracing:", os.getenv("LANGCHAIN_TRACING_V2"))
print("Project:", os.getenv("LANGCHAIN_PROJECT"))
print("API Key:", os.getenv("LANGCHAIN_API_KEY"))
print("MISTRAL_API_KEY:", os.getenv("MISTRAL_API_KEY"))
# ---- INITIALIZE ONCE (important for performance) ----

# Load vector database
vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10}
)

# LLM
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.2
# )
llm = ChatMistralAI(
    model="mistral-small",
    temperature=0.2
)

# Prompt
prompt = get_prompt()

# QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# ---- FUNCTION CALLED BY FLASK ----

def run_rag(question: str, report: str, history: list):

    # -----------------------------
    # 1. Retrieve using ONLY the latest user question
    # -----------------------------
    response = qa_chain.invoke({
        "question": question,
        "query": question
    })

    retrieved_context = response["result"]

    # -----------------------------
    # 2. Format previous conversation
    # -----------------------------
    history_text = ""

    for turn in history:
        history_text += (
            f"User: {turn['user']}\n"
            f"Assistant: {turn['assistant']}\n\n"
        )

    # -----------------------------
    # 3. Build final prompt
    # -----------------------------
    final_prompt = f"""
Medical Report:
{report if report else "No uploaded report."}

Previous Conversation:
{history_text if history_text else "No previous conversation."}

Relevant Medical Knowledge:
{retrieved_context}

Current User Question:
{question}
"""

    # -----------------------------
    # 4. Generate final response
    # -----------------------------
    final_response = llm.invoke(final_prompt)

    result = {
        "answer": final_response.content,
        "sources": []
    }

    # -----------------------------
    # 5. Return retrieved sources
    # -----------------------------
    if "source_documents" in response:
        for doc in response["source_documents"]:
            result["sources"].append(
                doc.metadata.get("test", "unknown")
            )

    return result




# from dotenv import load_dotenv
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain_community.llms import HuggingFacePipeline

# import torch

# from langchain_classic.chains import RetrievalQA
# from rag.load_vectorstore import load_vectorstore
# from rag.prompt import get_prompt



# # Load env vars (OPENAI_API_KEY)
# load_dotenv()

# # ---- INITIALIZE ONCE (important for performance) ----

# # Load vector database
# vectorstore = load_vectorstore()
# model_name = "mistralai/Mistral-7B-Instruct-v0.2"


# tokenizer = AutoTokenizer.from_pretrained(model_name)

# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     load_in_4bit=True,
#     device_map="auto",
#     torch_dtype=torch.float16
# )

# pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=512,
#     temperature=0.3,
#     top_p=0.9,
#     do_sample=True
# )

# llm = HuggingFacePipeline(pipeline=pipe)

# retriever = vectorstore.as_retriever(
#     search_type="mmr",
#     search_kwargs={"k": 4, "fetch_k": 10}
# )

# # LLM
# # llm = ChatOpenAI(
# #     model="gpt-4o-mini",
# #     temperature=0.2
# # )

# # Prompt
# prompt = get_prompt()

# # QA Chain
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     chain_type="stuff",
#     chain_type_kwargs={"prompt": prompt},
#     return_source_documents=True
# )

# # ---- FUNCTION CALLED BY FLASK ----

# def run_rag(question: str):
#     response = qa_chain.invoke({
#         "question": question,
#         "query": question
#     })

#     result = {
#         "answer": response["result"],
#         "sources": []
#     }

#     if "source_documents" in response:
#         for doc in response["source_documents"]:
#             result["sources"].append(
#                 doc.metadata.get("test", "unknown")
#             )

#     return result
