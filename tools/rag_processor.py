import os
import chromadb
from chromadb.api.types import Documents, Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_API_KEY
import boto3

# ---------- S3 CONFIG ----------
S3_BUCKET = "resume-rag-storage-preena-2026"
s3 = boto3.client("s3")


# ---------- EMBEDDING WRAPPER ----------
class ChromaLangchainEmbeddingFunction:
    def __init__(self, api_key):
        self.embedder = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )

    def __call__(self, input: Documents) -> Embeddings:
        # Chroma expects list of vectors
        return self.embedder.embed_documents(input)


# ---------- VAULT ----------
class ResumeVault:
    def __init__(self, persist_directory="./db/resume_vault"):
        os.makedirs(persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(path=persist_directory)

        self.embedding_function = ChromaLangchainEmbeddingFunction(
            api_key=GOOGLE_API_KEY
        )

        self.collection = self.client.get_or_create_collection(
            name="resumes",
            embedding_function=self.embedding_function
        )

    def add_resume(self, resume_text, metadata):
        """Add resume, upload to S3, and store embedding."""

        resume_id = metadata.get("id", os.urandom(4).hex())
        file_name = f"{resume_id}.txt"

        # Upload to S3
        try:
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=file_name,
                Body=resume_text
            )
        except Exception as e:
            print("S3 upload failed:", e)

        metadata["s3_url"] = f"https://{S3_BUCKET}/{file_name}"

        # Store in Chroma
        self.collection.add(
            documents=[resume_text],
            metadatas=[metadata],
            ids=[resume_id]
        )

        return resume_id

    def search_similar_resumes(self, query_text, n_results=3):
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

    def get_all_resumes(self):
        return self.collection.get()

    def clear_vault(self):
        self.client.delete_collection(name="resumes")

        self.collection = self.client.get_or_create_collection(
            name="resumes",
            embedding_function=self.embedding_function
        )

        return True


# ---------- GLOBAL INSTANCE ----------
vault = ResumeVault()