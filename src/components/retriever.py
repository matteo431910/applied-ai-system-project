"""Retriever Component - Searches knowledge base"""

from typing import List, Dict, Any
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from src.config.settings import settings
from src.utils.logger import get_logger


logger = get_logger(__name__)


class Retriever:
    """Retrieves relevant documents from knowledge base using semantic search"""
    
    def __init__(self, index=None):
        """
        Initialize retriever
        
        Args:
            index: Pinecone index instance
        """
        try:
            # Initialize embedding model (local, no API key needed)
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded local embedding model: all-MiniLM-L6-v2")
            
            self.index = index
            self.pc = None
            self._connected = False
            
            # Only initialize Pinecone if index is provided
            if index is not None:
                self._connected = True
                logger.info("Retriever initialized with provided index")
            else:
                logger.info("Retriever initialized (Pinecone connection will be lazy-loaded)")
        except Exception as e:
            logger.error(f"Failed to initialize Retriever: {str(e)}")
            raise
    
    def _ensure_connected(self):
        """Lazy load Pinecone connection on first use"""
        if self._connected:
            return
            
        try:
            if self.index is None:
                logger.info("Connecting to Pinecone...")
                self.pc = Pinecone(api_key=settings.pinecone_api_key)
                self.index = self.pc.Index(settings.pinecone_index_name)
                logger.info(f"Connected to Pinecone index: {settings.pinecone_index_name}")
            self._connected = True
        except Exception as e:
            logger.warning(f"Could not connect to Pinecone: {str(e)}")
            self.index = None
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Student query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        logger.info(f"Retrieving documents for query: {query}")
        
        try:
            # Query Pinecone index
            if self.index is None:
                logger.warning("Pinecone index not available, returning empty results")
                return []
            
            # Generate embedding for the query using local model
            query_embedding = self.embedding_model.encode(query).tolist()
            logger.debug(f"Generated query embedding with dimension: {len(query_embedding)}")
            
            # Search the index
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Parse results
            documents = []
            if results and results.get('matches'):
                for match in results['matches']:
                    doc = {
                        "title": match.get('metadata', {}).get('title', 'Unknown'),
                        "content": match.get('metadata', {}).get('content', ''),
                        "type": match.get('metadata', {}).get('type', 'document'),
                        "relevance_score": match.get('score', 0)
                    }
                    documents.append(doc)
            
            logger.info(f"Retrieved {len(documents)} documents from Pinecone")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Index documents in Pinecone
        
        Args:
            documents: Documents to index
        """
        logger.info(f"Indexing {len(documents)} documents")
        
        try:
            if self.index is None:
                logger.error("Pinecone index not available, cannot index documents")
                return
            
            # Prepare vectors for indexing
            vectors_to_upsert = []
            for i, doc in enumerate(documents):
                # Generate embedding for the document content
                content = doc.get("content", "") or doc.get("title", "")
                doc_embedding = self.embedding_model.encode(content).tolist()
                
                vector = {
                    "id": f"doc_{i}",
                    "values": doc_embedding,
                    "metadata": {
                        "title": doc.get("title", ""),
                        "content": doc.get("content", ""),
                        "type": doc.get("type", "document")
                    }
                }
                vectors_to_upsert.append(vector)
            
            # Upsert vectors into Pinecone
            self.index.upsert(vectors=vectors_to_upsert)
            logger.info(f"Successfully indexed {len(documents)} documents in Pinecone")
            
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            raise
