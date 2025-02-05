import os
import pinecone
import getpass
import time
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pprint import pprint
from pinecone import Pinecone, ServerlessSpec
from uuid import uuid4


def init_pinecone(index_name="web-rag"):

    if not os.getenv("PINECONE_API_KEY"):
        os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")

    pinecone_api_key = os.environ.get("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

    # 检查索引是否存在，不存在则创建（需匹配嵌入维度）
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI text-embedding-3-small为1536维
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    
    index = pc.Index(index_name)

    return index

def fetch_webpage(urls):
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
    docs, unwanted_tags=["script", "style", "header", "footer", "nav", "aside"], tags_to_extract=["p"]
    )
    return docs_transformed

def split_text(text, chunk_size=512, chunk_overlap=50):
    """使用 LangChain 进行文本分块"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(text)
    
    return chunks

# 主流程函数
def process_websites(urls: list, index_name: str = "web-rag"):
    # Step 1: 批量抓取网页并提取正文
    print("开始抓取网页...")
    docs_transformed = fetch_webpage(urls)

    # Step 2: 合并文本并分块（优化后的拆分逻辑）
    print("文本分块处理...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=100
    )

    chunks_with_metadata = []
    for doc in docs_transformed:
        # 拆分文本并附加元数据
        chunks = text_splitter.split_text(doc.page_content)
        for chunk in chunks:
            chunks_with_metadata.append({
                "text": chunk,
                "metadata": {
                    "source": doc.metadata["source"],
                    "title": doc.metadata["title"],
                }
            })

    # Step 3: 向量化并存储到Pinecone
    print("向量化并存储到Pinecone...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 将数据转换为Document格式
    documents = [
        Document(page_content=item["text"], metadata=item["metadata"])
        for item in chunks_with_metadata
    ]

    uuids = [str(uuid4()) for _ in range(len(documents))]

    # 批量存储到Pinecone
    PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name,
        ids=uuids
    )
    print(f"✅ 成功存储 {len(documents)} 个块到索引 {index_name}")

if __name__ == "__main__":
    # 初始化Pinecone
    # index_name = init_pinecone()
    # print(f"使用索引 {index_name} 存储数据")

    # # 🚀 开始爬取
    # base_url = ["https://d2l.ai/chapter_natural-language-processing-pretraining/bert.html",
    #             "https://zh.d2l.ai/chapter_natural-language-processing-pretraining/bert-pretraining.html"]
    # process_websites(base_url)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = PineconeVectorStore(index_name="web-rag", embedding=embeddings)
    results = vector_store.similarity_search(
    "Masked Language Modeling",
    k=2,
    # filter={"source": "tweet"},
)
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")
