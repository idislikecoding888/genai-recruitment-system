import os
import chromadb
from google import genai
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from config import GOOGLE_API_KEY

class GoogleGenAIEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_key, model_name="models/gemini-embedding-001"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def __call__(self, input: Documents) -> Embeddings:
        """Generate embeddings for the provided documents."""
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=input
        )
        # Extract embeddings as a list of lists of floats
        return [e.values for e in response.embeddings]

class ResumeVault:
    def __init__(self, persist_directory="./db/resume_vault"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use our custom Google GenAI embedding function to avoid deprecation warnings
        self.embedding_function = GoogleGenAIEmbeddingFunction(
            api_key=GOOGLE_API_KEY,
            model_name="models/gemini-embedding-001"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="resumes",
            embedding_function=self.embedding_function
        )

    def add_resume(self, resume_text, metadata):
        """Add a resume to the vault."""
        resume_id = metadata.get("id", str(os.urandom(4).hex()))
        self.collection.add(
            documents=[resume_text],
            metadatas=[metadata],
            ids=[resume_id]
        )
        return resume_id

    def search_similar_resumes(self, query_text, n_results=3):
        """Search for similar resumes in the vault."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

    def get_all_resumes(self):
        """Retrieve all resumes from the vault."""
        return self.collection.get()

    def clear_vault(self):
        """Delete all resumes from the vault."""
        # Deleting and recreating the collection is the most effective reset
        self.client.delete_collection(name="resumes")
        self.collection = self.client.get_or_create_collection(
            name="resumes",
            embedding_function=self.embedding_function
        )
        return True

# Global instance
vault = ResumeVault()
