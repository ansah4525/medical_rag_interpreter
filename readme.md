# Lab LLM RAG

This project implements a retrieval-augmented generation (RAG) pipeline
for interpreting laboratory test results using structured medical knowledge.

## Features
- Deterministic JSON chunking
- Chroma vector database
- Semantic retrieval (MMR)
- Balanced medical LLM prompting
- CLI-based testing (VS Code friendly)

## Setup
1. Copy `.env.example` → `.env`
2. Add your API key
3. Run `build_vectorstore.py`
4. Run `test_llm.py`

## Notes
This system provides educational explanations only and does not diagnose
or recommend medical treatments.
