import fitz
import re
import numpy as np
import faiss

from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI()

# -------------------------
# Load PDF
# -------------------------

pdf_path = "example.pdf"

doc = fitz.open(pdf_path)
text = ""

for page in doc:
    text += page.get_text()

# -------------------------
# Chunking
# -------------------------

def chunk_text(text, max_chunk_size=1000, overlap=200):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = current_chunk[-overlap:] + " " + sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


chunks = chunk_text(text)

# -------------------------
# Embeddings
# -------------------------

embedding_model = SentenceTransformer('all-mpnet-base-v2')
embeddings = embedding_model.encode(chunks)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# -------------------------
# Retrieval
# -------------------------

def retrieve(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]

# -------------------------
# LLM
# -------------------------

gen_model_name = "google/flan-t5-large"

tokenizer = AutoTokenizer.from_pretrained(gen_model_name)
generation_model = AutoModelForSeq2SeqLM.from_pretrained(gen_model_name)

def generate_answer(context, question):

    prompt = f"""
You are an expert assistant.

Carefully read the context and answer the question completely.

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    outputs = generation_model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.2,
        do_sample=False
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# -------------------------
# API Endpoint
# -------------------------

@app.get("/ask")

def ask(question: str):

    retrieved_chunks = retrieve(question, top_k=6)
    context = " ".join(retrieved_chunks)

    answer = generate_answer(context, question)

    return {
        "question": question,
        "answer": answer,
        "chunks_used": retrieved_chunks
    }