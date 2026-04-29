# Getting Started with College Major RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system to help college students find the best courses, resources, and career paths for their major.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com
- `PINECONE_API_KEY` - Get from https://www.pinecone.io

### 3. Run the Application

```bash
python -m src.main
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
src/
├── components/          # RAG system components
│   ├── retriever.py    # Semantic search
│   ├── agent.py        # LLM orchestration
│   └── evaluator.py    # Quality checks
├── config/             # Configuration
├── schemas/            # Data models
└── main.py            # FastAPI app

data/sample_data/      # Sample course and resource data
tests/                 # Unit tests
docs/API_ENDPOINTS.md  # API documentation
assets/                # Architecture diagrams
```

## Key Components

### Retriever
Searches the knowledge base for relevant courses, resources, and career information using semantic search.

### Agent
Orchestrates the recommendation process using Claude AI to generate personalized guidance based on student context.

### Evaluator
Quality-checks recommendations for accuracy, relevance, and career alignment.

## API Usage Example

```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What courses should I take for machine learning?",
    "major": "Computer Science",
    "academic_year": 2,
    "interests": ["AI", "Data Science"],
    "career_goals": "ML Engineer at a tech company"
  }'
```

## Next Steps

1. **Configure your API keys** in `.env`
2. **Explore the API** at `http://localhost:8000/docs`
3. **Review the architecture** in `assets/RAG_System_Architecture.mmd`
4. **Check API endpoints** in `docs/API_ENDPOINTS.md`
5. **Run tests** with `pytest tests/`

## Architecture Diagram

The system follows the RAG pattern:
1. **Input** → Student query
2. **Retrieval** → Find relevant materials
3. **Augmentation** → Enhance with reasoning
4. **Generation** → Create recommendations
5. **Evaluation** → Quality check
6. **Human Review** → Advisor feedback

See `assets/RAG_System_Architecture.mmd` for the complete architecture.

## Support

For issues or questions, check the documentation or review the API docs at `/docs` when the server is running.
