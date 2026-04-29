"""Helper functions"""

from typing import List, Dict, Any


def format_context(documents: List[Dict[str, Any]]) -> str:
    """Format retrieved documents into context string"""
    
    if not documents:
        return "No relevant documents found."
    
    context = "Retrieved Documents:\n\n"
    for i, doc in enumerate(documents, 1):
        context += f"{i}. {doc.get('title', 'Untitled')}\n"
        context += f"   {doc.get('content', '')}\n\n"
    
    return context


def parse_recommendations(text: str) -> List[str]:
    """Parse recommendations from LLM response"""
    
    # Simple parsing - can be enhanced
    lines = text.split('\n')
    recommendations = [line.strip() for line in lines if line.strip() and line.strip().startswith('-')]
    return recommendations
