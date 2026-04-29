"""pytest configuration and fixtures"""

import pytest
from src.components.retriever import Retriever
from src.components.agent import Agent
from src.components.evaluator import Evaluator


@pytest.fixture
def retriever():
    """Fixture providing a Retriever instance"""
    return Retriever()


@pytest.fixture
def agent():
    """Fixture providing an Agent instance"""
    return Agent()


@pytest.fixture
def evaluator():
    """Fixture providing an Evaluator instance"""
    return Evaluator()


@pytest.fixture
def sample_student_context():
    """Fixture providing sample student context"""
    return {
        "major": "Computer Science",
        "academic_year": 2,
        "gpa": 3.8,
        "interests": ["AI", "Data Science"],
        "career_goals": "ML Engineer"
    }


@pytest.fixture
def sample_documents():
    """Fixture providing sample documents"""
    return [
        {
            "title": "Machine Learning Fundamentals",
            "content": "Introduction to ML algorithms and applications"
        },
        {
            "title": "Advanced Python Programming",
            "content": "Python best practices and advanced techniques"
        }
    ]
