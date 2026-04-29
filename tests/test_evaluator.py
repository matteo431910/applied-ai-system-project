"""Tests for Evaluator component"""

import pytest
from src.components.evaluator import Evaluator


def test_evaluator_initialization():
    """Test Evaluator initialization"""
    evaluator = Evaluator()
    assert evaluator is not None
    assert evaluator.model == "claude-3-sonnet-20240229"


def test_extract_score():
    """Test score extraction from evaluation text"""
    evaluator = Evaluator()
    
    test_text = "Quality score 85 out of 100. This is good."
    score = evaluator._extract_score(test_text)
    
    # Score should be normalized to 0-1
    assert 0 <= score <= 1


def test_extract_score_default():
    """Test default score when no score found"""
    evaluator = Evaluator()
    
    test_text = "This is a good recommendation"
    score = evaluator._extract_score(test_text)
    
    # Should return default score
    assert score == 0.7
