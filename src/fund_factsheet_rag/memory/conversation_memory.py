"""
Memory layer for conversation history using FAISS
Stores and retrieves relevant past conversations
"""
from langchain_community.vectorstores import FAISS
from langchain.schema import Document, BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
import yaml
import os
import pickle
from pathlib import Path
from datetime import datetime
from ..embeddings.text_encoder import get_embeddings

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

_memory_store = None
_conversation_memory = None

class ConversationMemoryManager:
    """
    Manages conversation history with FAISS-based semantic search
    Allows retrieval of relevant past conversations
    """

    def __init__(self):
        self.memory_path = CFG["paths"]["memory_index"]
        Path(self.memory_path).mkdir(parents=True, exist_ok=True)

        self.embeddings = get_embeddings()
        self.memory_file = os.path.join(self.memory_path, "memory.faiss")
        self.conversations_file = os.path.join(self.memory_path, "conversations.pkl")

        # Load or create memory store
        if os.path.exists(self.memory_file):
            self.memory_store = FAISS.load_local(
                self.memory_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            # Load conversations
            if os.path.exists(self.conversations_file):
                with open(self.conversations_file, 'rb') as f:
                    self.conversations = pickle.load(f)
            else:
                self.conversations = []
        else:
            # Create empty memory store
            self.memory_store = FAISS.from_documents(
                [Document(page_content="initialization", metadata={"type": "init"})],
                self.embeddings
            )
            self.conversations = []

        self.max_history = CFG["memory"]["max_history"]

    def add_conversation_turn(self, user_message: str, assistant_message: str, metadata: dict = None):
        """
        Add a conversation turn to memory

        Args:
            user_message: User's question
            assistant_message: Assistant's response
            metadata: Optional metadata (sources, etc.)
        """
        timestamp = datetime.now().isoformat()

        # Create conversation document
        conversation_text = f"User: {user_message}\nAssistant: {assistant_message}"

        doc_metadata = {
            "timestamp": timestamp,
            "user_message": user_message,
            "assistant_message": assistant_message,
            "type": "conversation"
        }

        if metadata:
            doc_metadata.update(metadata)

        document = Document(
            page_content=conversation_text,
            metadata=doc_metadata
        )

        # Add to FAISS memory store
        self.memory_store.add_documents([document])

        # Add to conversations list
        self.conversations.append({
            "user": user_message,
            "assistant": assistant_message,
            "timestamp": timestamp,
            "metadata": metadata or {}
        })

        # Keep only recent conversations in memory
        if len(self.conversations) > self.max_history:
            self.conversations = self.conversations[-self.max_history:]

        # Save to disk
        self.save_memory()

    def get_relevant_history(self, query: str, k: int = 3) -> list:
        """
        Retrieve relevant past conversations based on semantic similarity

        Args:
            query: Current user query
            k: Number of relevant conversations to retrieve

        Returns:
            List of relevant conversation turns
        """
        try:
            results = self.memory_store.similarity_search_with_score(query, k=k)

            # Filter out initialization document and format results
            relevant_conversations = []
            for doc, score in results:
                if doc.metadata.get("type") != "init":
                    relevant_conversations.append({
                        "conversation": doc.page_content,
                        "metadata": doc.metadata,
                        "relevance_score": float(score)
                    })

            return relevant_conversations
        except Exception as e:
            print(f"Error retrieving relevant history: {e}")
            return []

    def get_recent_history(self, n: int = 5) -> list:
        """
        Get the n most recent conversation turns

        Args:
            n: Number of recent turns to retrieve

        Returns:
            List of recent conversation turns
        """
        return self.conversations[-n:] if self.conversations else []

    def get_conversation_context(self, query: str, include_recent: int = 3, include_relevant: int = 2) -> str:
        """
        Get formatted conversation context combining recent and relevant history

        Args:
            query: Current query
            include_recent: Number of recent turns to include
            include_relevant: Number of semantically relevant turns to include

        Returns:
            Formatted conversation context string
        """
        context_parts = []

        # Get recent history
        recent = self.get_recent_history(include_recent)
        if recent:
            context_parts.append("Recent conversation:")
            for conv in recent:
                context_parts.append(f"User: {conv['user']}")
                context_parts.append(f"Assistant: {conv['assistant'][:200]}...")

        # Get relevant history (excluding what's already in recent)
        relevant = self.get_relevant_history(query, k=include_relevant)
        if relevant:
            context_parts.append("\nRelevant past conversations:")
            for conv in relevant:
                context_parts.append(conv['conversation'][:300] + "...")

        return "\n".join(context_parts)

    def save_memory(self):
        """Save memory to disk"""
        try:
            self.memory_store.save_local(self.memory_path)
            with open(self.conversations_file, 'wb') as f:
                pickle.dump(self.conversations, f)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def clear_memory(self):
        """Clear all conversation history"""
        self.conversations = []
        self.memory_store = FAISS.from_documents(
            [Document(page_content="initialization", metadata={"type": "init"})],
            self.embeddings
        )
        self.save_memory()

def get_memory_manager():
    """Get or create memory manager instance"""
    global _memory_store
    if _memory_store is None:
        _memory_store = ConversationMemoryManager()
    return _memory_store
