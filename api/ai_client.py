"""
AI Microservice Client for Nostalgia Django App
================================================
Communicates with the FastAPI AI Embedding Microservice (D:\\DEV\\AI\\embedding_generator)
running at http://ai_embedding_generator:8002 (or http://localhost:8002).
"""

import os
import requests
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

                                                                                             
AI_SERVICE_URL = os.environ.get("AI_SERVICE_URL", "http://localhost:8002")


class AIEmbeddingClient:
    """Client wrapper to request vector embeddings and similarity scores."""

    @staticmethod
    def is_service_available() -> bool:
        """Check if AI embedding microservice is active."""
        try:
            res = requests.get(f"{AI_SERVICE_URL}/health", timeout=2)
            return res.status_code == 200
        except Exception:
            return False

    @staticmethod
    def get_text_embedding(text: str) -> List[float]:
        """Request 384-dimensional vector embedding for text."""
        try:
            res = requests.post(f"{AI_SERVICE_URL}/embed", json={"text": text}, timeout=4)
            if res.status_code == 200:
                return res.json().get("vector", [])
        except Exception as e:
            logger.warning(f"AI Service embed call failed: {e}")
        return []

    @staticmethod
    def get_user_embedding(user_data: Dict[str, Any]) -> List[float]:
        """Request 384-dimensional vector embedding for User Profile."""
        try:
            res = requests.post(f"{AI_SERVICE_URL}/embed/user", json=user_data, timeout=4)
            if res.status_code == 200:
                return res.json().get("vector", [])
        except Exception as e:
            logger.warning(f"AI Service user embed call failed: {e}")
        return []

    @staticmethod
    def get_post_embedding(post_data: Dict[str, Any]) -> List[float]:
        """Request 384-dimensional vector embedding for Feed Post."""
        try:
            res = requests.post(f"{AI_SERVICE_URL}/embed/post", json=post_data, timeout=4)
            if res.status_code == 200:
                return res.json().get("vector", [])
        except Exception as e:
            logger.warning(f"AI Service post embed call failed: {e}")
        return []

    @staticmethod
    def get_group_embedding(group_data: Dict[str, Any]) -> List[float]:
        """Request 384-dimensional vector embedding for Community Group."""
        try:
            res = requests.post(f"{AI_SERVICE_URL}/embed/group", json=group_data, timeout=4)
            if res.status_code == 200:
                return res.json().get("vector", [])
        except Exception as e:
            logger.warning(f"AI Service group embed call failed: {e}")
        return []

    @staticmethod
    def get_event_embedding(event_data: Dict[str, Any]) -> List[float]:
        """Request 384-dimensional vector embedding for Walk / Trip event."""
        try:
            res = requests.post(f"{AI_SERVICE_URL}/embed/event", json=event_data, timeout=4)
            if res.status_code == 200:
                return res.json().get("vector", [])
        except Exception as e:
            logger.warning(f"AI Service event embed call failed: {e}")
        return []

    @staticmethod
    def compute_similarity(vector1: List[float], vector2: List[float]) -> float:
        """Request cosine similarity score (-1.0 to 1.0) between two vectors."""
        try:
            res = requests.post(
                f"{AI_SERVICE_URL}/similarity",
                json={"vector1": vector1, "vector2": vector2},
                timeout=4
            )
            if res.status_code == 200:
                return res.json().get("similarity", 0.0)
        except Exception as e:
            logger.warning(f"AI Service similarity call failed: {e}")
        return 0.0
