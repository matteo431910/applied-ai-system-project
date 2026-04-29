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


def test_extract_confidence():
    """Test confidence extraction from evaluation text"""
    evaluator = Evaluator()
    
    test_text = "Quality score 85 out of 100. Confidence level: 90 out of 100."
    confidence = evaluator._extract_confidence(test_text)
    
    # Confidence should be normalized to 0-1
    assert 0 <= confidence <= 1
    assert confidence > 0.8  # Should be high confidence


def test_extract_confidence_default():
    """Test default confidence when not found"""
    evaluator = Evaluator()
    
    test_text = "This is a good recommendation"
    confidence = evaluator._extract_confidence(test_text)
    
    # Should return default confidence
    assert confidence == 0.75
