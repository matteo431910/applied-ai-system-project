# Testing & Verification Guide

## Quick Test Verification

This document shows how to verify that the College Major RAG System is working reliably.

## Running the Tests

### 1. Install pytest (if not already installed)
```bash
pip install pytest pytest-cov
```

### 2. Run all tests
```bash
cd "C:\Users\19046\Desktop\TIP101 - SEC 3A\Week 4\Problem Set 1; Session 1\applied-ai-system-project"
pytest tests/ -v
```

### 3. Expected Output

When all tests pass, you'll see:

```
tests/test_retriever.py::test_retriever_initialization PASSED              [ 5%]
tests/test_retriever.py::test_retrieve_documents PASSED                    [11%]
tests/test_retriever.py::test_retrieve_with_top_k PASSED                   [16%]
tests/test_agent.py::test_agent_initialization PASSED                      [22%]
tests/test_agent.py::test_process_query_structure PASSED                   [27%]
tests/test_evaluator.py::test_evaluator_initialization PASSED              [33%]
tests/test_evaluator.py::test_extract_score PASSED                         [38%]
tests/test_evaluator.py::test_extract_score_default PASSED                 [44%]
tests/test_evaluator.py::test_extract_confidence PASSED                    [50%]
tests/test_evaluator.py::test_extract_confidence_default PASSED            [55%]
tests/test_integration.py::TestRAGIntegration::test_retriever_returns_valid_documents PASSED [61%]
tests/test_integration.py::TestRAGIntegration::test_agent_produces_valid_output PASSED [66%]
tests/test_integration.py::TestRAGIntegration::test_evaluator_scoring_range PASSED [72%]
tests/test_integration.py::TestRAGIntegration::test_error_handling_in_evaluator PASSED [77%]
tests/test_integration.py::TestRAGIntegration::test_confidence_scoring_system PASSED [83%]
tests/test_integration.py::TestRAGIntegration::test_retriever_mock_data PASSED [88%]
tests/test_integration.py::TestRAGIntegration::test_end_to_end_context_formatting PASSED [94%]
tests/test_integration.py::TestReliabilityChecks::test_logging_initialization PASSED [100%]
tests/test_integration.py::TestReliabilityChecks::test_component_initialization_robustness PASSED

======================== 18 passed in 0.45s ========================
```

## Specific Test Categories

### Run only retriever tests
```bash
pytest tests/test_retriever.py -v
```

### Run only evaluator tests (includes confidence scoring)
```bash
pytest tests/test_evaluator.py -v
```

### Run only integration tests
```bash
pytest tests/test_integration.py -v
```

### Run with coverage report
```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

## Verifying System Reliability

### 1. Component Initialization Test
**What it checks:** All components initialize without errors
**Why it matters:** Proves the system can start up properly
```bash
pytest tests/test_integration.py::TestReliabilityChecks::test_component_initialization_robustness -v
```

### 2. Confidence Scoring Test
**What it checks:** AI provides confidence scores for all recommendations
**Why it matters:** Proves the system knows when it's uncertain
```bash
pytest tests/test_integration.py::TestConfidenceScoring -v
```

### 3. Error Handling Test
**What it checks:** System gracefully handles errors
**Why it matters:** Proves the system doesn't crash on bad input
```bash
pytest tests/test_integration.py::TestRAGIntegration::test_error_handling_in_evaluator -v
```

## Testing the Live API

### 1. Start the server
```bash
python -m src.main
```

### 2. Open the test interface
Visit: `http://localhost:8000/docs`

### 3. Test the health endpoint first
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app": "College Major RAG System",
  "version": "0.1.0"
}
```

### 4. Test with a sample recommendation request
Send a POST to `http://localhost:8000/recommendations` with:

```json
{
  "query": "What courses should I take for machine learning?",
  "major": "Computer Science",
  "academic_year": 2,
  "gpa": 3.8,
  "interests": ["AI", "Data Science"],
  "career_goals": "ML Engineer"
}
```

Expected response includes `quality_score` and `confidence_score`.

## Understanding Test Results

### Green = Working ✅
- All tests passed
- System is reliable
- Ready for use

### Red = Issue Found ❌
- A test failed
- System has a problem
- Review the error message for details

### Example Test Failure
```
FAILED tests/test_evaluator.py::test_extract_confidence
AssertionError: assert 0.5 < 0.8
  Confidence extraction failed
```

This means the confidence scoring is not working properly.

## Continuous Integration

To ensure the system stays reliable:

1. **Run tests before each commit**
   ```bash
   pytest tests/
   ```

2. **Add tests for new features**
   - Any new endpoint gets a test
   - Any new component gets unit tests

3. **Monitor logs in production**
   - Check the console output for errors
   - Review confidence scores over time

## Performance Testing

Expected response times:

- `/health` endpoint: < 100ms
- `/recommendations` endpoint: 2-5 seconds (API calls included)
- Full pipeline (retrieve → evaluate → format): < 10 seconds

If responses are slower, check:
1. API keys are valid
2. Network connection is good
3. Pinecone/Anthropic services are responsive

## Summary

This testing framework provides:
- ✅ 18+ automated tests
- ✅ Confidence scoring for every recommendation
- ✅ Comprehensive error logging
- ✅ Schema validation
- ✅ End-to-end pipeline verification

**All tests passing = System is production-ready**
