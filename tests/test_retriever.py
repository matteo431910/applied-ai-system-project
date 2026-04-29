"""Tests for Retriever component"""

import pytest
from src.components.retriever import Retriever


def test_retriever_initialization():
    """Test Retriever initialization"""
    retriever = Retriever()
    assert retriever is not None


def test_retrieve_documents():
    """Test document retrieval"""
    retriever = Retriever()
    results = retriever.retrieve("machine learning courses")
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert all("title" in doc for doc in results)
    assert all("content" in doc for doc in results)


def test_retrieve_with_top_k():
    """Test retrieval with custom top_k"""
    retriever = Retriever()
    results = retriever.retrieve("python programming", top_k=3)
    
    assert len(results) <= 3
