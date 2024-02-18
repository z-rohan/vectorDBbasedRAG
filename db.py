import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb.config import Settings
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    model = 'models/embedding-001'
    title = "Custom query"
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    return genai.embed_content(model=model,
                                content=input,
                                task_type="retrieval_document",
                                title=title)["embedding"]
  
class DB:
    def __init__(self):
       pass
    def create_and_upsert_chroma_db(self, documents):
        # chroma_client = chromadb.PersistentClient('.db/', settings=Settings(allow_reset=True))
        chroma_client = chromadb.Client()
        db = chroma_client.get_or_create_collection(name='got1', embedding_function=GeminiEmbeddingFunction())

        for i, d in enumerate(documents):
            db.upsert(
            documents=d,
            ids=str(i)
            )
        return db
    
    def delete_collection(self, db):
        db.delete()

    def get_coll(self):
        chroma_client = chromadb.Client()
        coll = chroma_client.get_collection('got1', embedding_function=GeminiEmbeddingFunction())
        return coll

    def get_relevant_passage(self, query):
        db = self.get_coll()
        passage = db.query(query_texts=query, n_results=3)['documents'][0]
        return passage