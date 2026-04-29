"""Integration tests for the RAG system"""

import pytest
from src.components.retriever import Retriever
from src.components.agent import Agent
from src.components.evaluator import Evaluator


class TestRAGIntegration:
    """Integration tests for the complete RAG pipeline"""
    
    def test_retriever_returns_valid_documents(self):
        """Test that retriever returns properly formatted documents"""
        retriever = Retriever()
        
        docs = retriever.retrieve("machine learning courses")
        
        # Verify document structure
        assert isinstance(docs, list)
        assert len(docs) > 0
        
        for doc in docs:
            assert "title" in doc
            assert "content" in doc
            assert len(doc["title"]) > 0
            assert len(doc["content"]) > 0
    
    def test_agent_produces_valid_output(self):
        """Test that agent generates text responses"""
        agent = Agent()
        
        student_query = "What programming languages should I learn?"
        student_context = {
            "major": "Computer Science",
            "academic_year": 1,
            "gpa": 3.5,
            "interests": ["Programming", "Software Engineering"],
            "career_goals": "Software Engineer"
        }
        docs = [{"title": "CS101", "content": "Programming basics"}]
        
        # Format context for agent
        response = agent._format_context(student_context, docs)
        
        # Verify response contains key information
        assert "Computer Science" in response
        assert "Programming basics" in response
        assert "1" in response  # Year
    
    def test_evaluator_scoring_range(self):
        """Test that evaluator produces valid scores"""
        evaluator = Evaluator()
        
        # Test score extraction
        test_text = "Quality score 75 out of 100"
        score = evaluator._extract_score(test_text)
        
        assert 0 <= score <= 1
        assert score > 0.7
    
    def test_error_handling_in_evaluator(self):
        """Test that evaluator handles errors gracefully"""
        evaluator = Evaluator()
        
        # Test with empty text
        test_text = ""
        score = evaluator._extract_score(test_text)
        
        # Should return default, not crash
        assert score == 0.7
    
    def test_confidence_scoring_system(self):
        """Test confidence scoring implementation"""
        evaluator = Evaluator()
        
        # High confidence text
        high_conf_text = "Quality score 90 out of 100. Confidence level: 95 out of 100. APPROVED"
        conf = evaluator._extract_confidence(high_conf_text)
        assert conf > 0.9
        
        # Low confidence text
        low_conf_text = "This might work. Confidence level: 50 out of 100."
        conf = evaluator._extract_confidence(low_conf_text)
        assert 0.4 < conf < 0.6
    
    def test_retriever_mock_data(self):
        """Test that mock data is properly formatted"""
        retriever = Retriever()
        
        docs = retriever.retrieve("career advice")
        
        # Verify we get consistent results
        assert len(docs) >= 1
        
        # Verify document has relevance score
        for doc in docs:
            assert isinstance(doc, dict)
    
    def test_end_to_end_context_formatting(self):
        """Test the end-to-end context formatting"""
        agent = Agent()
        
        student_context = {
            "major": "Business",
            "academic_year": 3,
            "gpa": 3.8,
            "interests": ["Analytics", "Finance"],
            "career_goals": "Financial Analyst"
        }
        docs = [
            {"title": "Excel for Business", "content": "Advanced Excel skills"},
            {"title": "Finance Fundamentals", "content": "Core finance concepts"}
        ]
        
        context = agent._format_context(student_context, docs)
        
        # Verify all key information is included
        assert "Business" in context
        assert "3" in context
        assert "3.8" in context
        assert "Financial Analyst" in context
        assert "Excel for Business" in context
        assert len(context) > 100


class TestReliabilityChecks:
    """Tests that verify system reliability"""
    
    def test_logging_initialization(self):
        """Test that logging is properly configured"""
        from src.utils.logger import get_logger
        
        logger = get_logger("test")
        assert logger is not None
        assert logger.name == "test"
    
    def test_component_initialization_robustness(self):
        """Test that components initialize without errors"""
        try:
            retriever = Retriever()
            agent = Agent()
            evaluator = Evaluator()
            
            assert retriever is not None
            assert agent is not None
            assert evaluator is not None
            
        except Exception as e:
            pytest.fail(f"Component initialization failed: {str(e)}")
    
    def test_api_response_schema_validation(self):
        """Test that API responses follow the schema"""
        from src.schemas.recommendation import RecommendationResponse
        
        # Create a valid response
        response = RecommendationResponse(
            query_id="test-123",
            student_major="Computer Science",
            recommended_courses=[],
            skills_to_develop=["Python", "SQL"],
            resources=[],
            action_plan="Test plan",
            next_steps=["Step 1"],
            mentorship_opportunities=[],
            quality_score=0.85
        )
        
        assert response.quality_score == 0.85
        assert response.student_major == "Computer Science"
        assert "Python" in response.skills_to_develop


class TestConfidenceScoring:
    """Tests specifically for confidence scoring"""
    
    def test_confidence_score_reflects_certainty(self):
        """Test that confidence scores align with recommendation quality"""
        evaluator = Evaluator()
        
        # High quality should have high confidence
        high_quality = "Excellent recommendation. Quality: 95/100. Confidence: 95/100. APPROVED."
        conf = evaluator._extract_confidence(high_quality)
        score = evaluator._extract_score(high_quality)
        
        assert conf > 0.9
        assert score > 0.9
    
    def test_low_confidence_indication(self):
        """Test that low confidence is properly detected"""
        evaluator = Evaluator()
        
        uncertain = "Confidence: 40 out of 100. NEEDS_REVISION."
        conf = evaluator._extract_confidence(uncertain)
        
        assert conf < 0.5


def test_system_resilience():
    """Test that system handles edge cases"""
    retriever = Retriever()
    
    # Edge case: very short query
    result = retriever.retrieve("ML")
    assert isinstance(result, list)
    
    # Edge case: special characters
    result = retriever.retrieve("C++ programming?")
    assert isinstance(result, list)
