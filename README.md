# WebRAG: AI-Powered Web Knowledge Retrieval & QA 🚀  

An AI-powered retrieval-augmented generation (RAG) system that extracts information from webpages, processes it using a vector database, and generates intelligent responses via a Large Language Model (LLM).  

## 📌 Features  
- **🔗 Web Scraping**: Extracts text from web pages using BeautifulSoup and requests.  
- **📂 Text Processing**: Cleans and chunks text for vector storage.  
- **🔍 Hybrid Retrieval**: Combines keyword-based (BM25) and dense retrieval (FAISS/Pinecone).  
- **🤖 LLM Integration**: Uses OpenAI/GPT API for intelligent response generation.  
- **⚡ Fast API Service**: Deploys as an API with FastAPI for easy integration.  
- **📦 Dockerized Deployment**: Ready for cloud deployment (AWS/GCP).  

---

## 📂 Project Structure  

```bash
WebRAG/
│── data/                 # Store scraped web data (optional)
│── embeddings/           # Store FAISS/Pinecone vectors
│── models/               # Fine-tuned models (if applicable)
│── src/
│   ├── scraper.py        # Web scraping module
│   ├── preprocess.py     # Text cleaning and chunking
│   ├── embedder.py       # Sentence embedding (e.g., MiniLM, Ada-002)
│   ├── retriever.py      # Hybrid retrieval (BM25 + FAISS)
│   ├── generator.py      # LLM-based response generation
│   ├── api.py            # FastAPI service
│── notebooks/            # Jupyter notebooks for testing
│── docker/               # Docker deployment files
│── requirements.txt      # Dependencies
│── README.md             # Project Documentation
