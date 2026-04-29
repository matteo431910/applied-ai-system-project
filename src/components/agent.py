"""Agent Component - Orchestrates recommendations"""

from typing import Dict, Any
from anthropic import Anthropic
from src.config.settings import settings
from src.config.prompts import SYSTEM_PROMPT
from src.utils.logger import get_logger


logger = get_logger(__name__)


class Agent:
    """Agent that orchestrates the RAG system and generates recommendations"""
    
    def __init__(self):
        """Initialize Agent with Anthropic client"""
        self.client = Anthropic()
        self.model = "claude-3-sonnet-20240229"
        logger.info("Agent initialized with Claude")
    
    def process_query(self, 
                     student_query: str, 
                     student_context: Dict[str, Any],
                     retrieved_documents: list) -> str:
        """
        Process student query and generate recommendations
        
        Args:
            student_query: The student's question
            student_context: Context about the student (major, year, etc)
            retrieved_documents: Retrieved relevant documents
            
        Returns:
            Generated recommendation text
        """
        logger.info("Processing query through Agent")
        
        # Format context for prompt
        context_text = self._format_context(student_context, retrieved_documents)
        
        # Build message for Claude
        messages = [
            {
                "role": "user",
                "content": f"{context_text}\n\nStudent Query: {student_query}\n\nProvide personalized recommendations."
            }
        ]
        
        # Get response from Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=settings.max_tokens,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        
        recommendation_text = response.content[0].text
        logger.info("Agent generated recommendations")
        
        return recommendation_text
    
    def _format_context(self, student_context: Dict[str, Any], documents: list) -> str:
        """Format context for the prompt"""
        
        context = f"""
Student Profile:
- Major: {student_context.get('major', 'Unknown')}
- Year: {student_context.get('academic_year', 'Unknown')}
- GPA: {student_context.get('gpa', 'Not provided')}
- Interests: {', '.join(student_context.get('interests', []))}
- Career Goals: {student_context.get('career_goals', 'Not specified')}

Retrieved Resources:
"""
        for doc in documents:
            context += f"- {doc.get('title', 'Untitled')}: {doc.get('content', '')}\n"
        
        return context
