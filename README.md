# PDF Assistant – RAG Based Question Answering System

## Overview

This project is an **AI-powered PDF Assistant** that allows users to ask questions about the contents of a PDF document and receive accurate answers.
The system uses **Retrieval-Augmented Generation (RAG)**, which combines semantic search with a language model to generate context-aware answers.

The application extracts text from a PDF, splits it into smaller chunks, converts those chunks into vector embeddings, stores them in a FAISS vector database, retrieves the most relevant chunks for a query, and then generates a final answer using a language model.

---

# Objectives

* Enable users to **ask questions about a PDF document**
* Retrieve the **most relevant information** from the document
* Generate **clear and complete answers**
* Provide an **automatic summary** of the entire document
* Package the system using **Docker for easy deployment**

---

# Working Principle

The system follows a **Retrieval-Augmented Generation (RAG) pipeline**:

1. **PDF Input**

   * The user uploads a PDF file.

2. **Text Extraction**

   * Text is extracted from the PDF using **PyMuPDF**.

3. **Text Chunking**

   * The document is split into smaller chunks to improve retrieval accuracy.

4. **Embedding Generation**

   * Each chunk is converted into a numerical vector representation using a sentence transformer model.

5. **Vector Storage**

   * All embeddings are stored in a **FAISS vector index** for fast similarity search.

6. **Query Processing**

   * When a user asks a question, the system converts the question into an embedding.

7. **Semantic Retrieval**

   * FAISS retrieves the most relevant text chunks based on similarity.

8. **Answer Generation**

   * The retrieved context and user question are given to a language model to generate the final answer.

9. **Document Summarization**

   * The system also summarizes each chunk and combines them into a final summary of the whole document.

---

# Technologies and Libraries Used

## Python

Used as the main programming language for building the entire pipeline.

## PyMuPDF (fitz)

Used for **extracting text from PDF documents**.

Purpose:

* Read PDF files
* Extract text page by page

---

## Regular Expressions (re)

Used for **splitting the extracted text into sentences**.

Purpose:

* Sentence tokenization
* Preparing text for chunking

---

## Sentence Transformers

Model used:

```
sentence-transformers/all-mpnet-base-v2
```

Purpose:

* Convert text chunks into **semantic embeddings**
* Enable similarity search between queries and document chunks

---

## FAISS (Facebook AI Similarity Search)

Purpose:

* Store embeddings efficiently
* Perform **fast similarity search**
* Retrieve the most relevant document chunks for a query

---

## Transformers (HuggingFace)

Model used:

```
google/flan-t5-large
```

Purpose:

* Generate answers based on retrieved context
* Summarize document chunks
* Produce natural language responses

---

## NumPy

Used for:

* Handling embedding vectors
* Converting embeddings into arrays for FAISS indexing

---

## FastAPI

Used to build the **API server** that allows the system to be accessed through HTTP requests.

Purpose:

* Serve the AI model as an API
* Allow users to send queries and receive answers

---

## Docker

Used to **containerize the application**.

Purpose:

* Ensure the application runs consistently on any system
* Package dependencies, models, and code together
* Simplify deployment

---

## VS Code

Used as the main **development environment** for running and managing the project locally.

---

# Project Workflow

```
PDF File
   ↓
Text Extraction (PyMuPDF)
   ↓
Sentence Splitting (Regex)
   ↓
Chunk Creation
   ↓
Embedding Generation (Sentence Transformers)
   ↓
Vector Storage (FAISS)
   ↓
User Question
   ↓
Query Embedding
   ↓
Relevant Chunk Retrieval
   ↓
Answer Generation (FLAN-T5)
```

---

# Running the Project with Docker

## Build the Docker Image

```
docker build -t pdfasst .
```

## Run the Container

```
docker run -p 8000:8000 pdfasst
```

## Access the API

Open in browser:

```
http://localhost:8000/docs
```

This opens the **FastAPI Swagger interface** where users can interact with the API.

---

# 🔍 Example Query

```
What is cryptography?
```

The system retrieves relevant information from the PDF and generates a clear answer using the language model.

---

# Document Summarization

The system also generates a **complete summary of the PDF** by:

1. Summarizing individual chunks
2. Combining them into a final overall summary

---

# Current Limitations

* Works with one PDF at a time
* Large models require more memory
* First run may take time due to model loading


---

# Author

Tharun P

---

# Project Type

Artificial Intelligence / Retrieval-Augmented Generation / Natural Language Processing


