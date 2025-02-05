# **WebRAG: A Retrieval-Augmented Generation (RAG) System for Web Content**

WebRAG is designed to extract content from a given sitemap, recursively find all sub-pages of a target website, clean and store the content in a vector database, and use it in a Retrieval-Augmented Generation (RAG) pipeline powered by LangChain. 

---
## 📂 **Project Structure**

```bash
WebRAG/
│── src/
│   ├── scraper.py        # Web scraping module
│   ├── preprocess.py     # Text cleaning and chunking
│   ├── embedder.py       # Sentence embedding (e.g., MiniLM, Ada-002)
│   ├── retriever.py      # Hybrid retrieval (BM25 + FAISS)
│   ├── generator.py      # LLM-based response generation
│   ├── api.py            # FastAPI service
│── WebRAG.ipynb          # Jupyter notebooks for testing
│── docker/               # Docker deployment files
│── requirements.txt      # Dependencies
│── README.md             # Project Documentation
```

---
## **1️⃣ Web Crawling**

Extract links from a sitemap using `/robots.txt` or `/sitemap.xml`. 

### Run the script  
```bash
python src/crawl.py --url "https://python.langchain.com/sitemap.xml" --filter "/docs/tutorials/"
```

### ✅ Output Example
```
🔗 Found 12 Pages in Sitemap:
https://python.langchain.com/docs/tutorials/
https://python.langchain.com/docs/tutorials/agents/
https://python.langchain.com/docs/tutorials/chatbot/
...
```

---
## 2️⃣ Embedding & Vector Storage

🔹 Goal

Convert extracted text into dense embeddings and store in FAISS/Pinecone for retrieval.

🔹 Steps
	1.	Choose Embedding Model: Use SentenceTransformers or OpenAI text-embedding-ada-002.
	2.	Vectorize Chunks: Convert text chunks to numerical embeddings.
	3.	Store in FAISS/Pinecone: Create an index for fast retrieval.