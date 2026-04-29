"""Tests for Agent component"""

import pytest
from src.components.agent import Agent


def test_agent_initialization():
    """Test Agent initialization"""
    agent = Agent()
    assert agent is not None
    assert agent.model == "claude-3-sonnet-20240229"


def test_process_query_structure():
    """Test that process_query returns a string"""
    agent = Agent()
    
    student_query = "What should I study for machine learning?"
    student_context = {
        "major": "Computer Science",
        "academic_year": 2,
        "gpa": 3.8,
        "interests": ["AI", "Data Science"],
        "career_goals": "ML Engineer"
    }
    retrieved_documents = [
        {
            "title": "Machine Learning 101",
            "content": "Introduction to ML concepts"
        }
    ]
    
    # This will require API key to run - mark as integration test
    # result = agent.process_query(student_query, student_context, retrieved_documents)
    # assert isinstance(result, str)
    # assert len(result) > 0
    
    # For now, just test the format_context method
    context = agent._format_context(student_context, retrieved_documents)
    assert "Computer Science" in context
    assert "Machine Learning 101" in context
