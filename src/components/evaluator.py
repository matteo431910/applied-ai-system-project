"""Evaluator Component - Quality checks recommendations"""

from typing import Dict, Any, Tuple
from anthropic import Anthropic
from src.config.settings import settings
from src.config.prompts import EVALUATOR_PROMPT
from src.utils.logger import get_logger


logger = get_logger(__name__)


class Evaluator:
    """Evaluates the quality of generated recommendations"""
    
    def __init__(self):
        """Initialize Evaluator with Anthropic client"""
        self.client = Anthropic()
        self.model = "claude-3-sonnet-20240229"
        logger.info("Evaluator initialized")
    
    def evaluate(self, 
                recommendation: str, 
                student_context: Dict[str, Any]) -> Tuple[float, str, bool]:
        """
        Evaluate recommendation quality
        
        Args:
            recommendation: The generated recommendation text
            student_context: Context about the student
            
        Returns:
            Tuple of (quality_score, feedback, approved)
        """
        logger.info("Evaluating recommendation")
        
        messages = [
            {
                "role": "user",
                "content": f"""
Student Major: {student_context.get('major')}
Career Goals: {student_context.get('career_goals')}

Recommendation:
{recommendation}

{EVALUATOR_PROMPT}

Provide:
1. Quality score (0-100)
2. Feedback on strengths and areas for improvement
3. Approval decision (APPROVED/NEEDS_REVISION)
"""
            }
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=messages
        )
        
        evaluation_text = response.content[0].text
        logger.info("Evaluation complete")
        
        # Parse evaluation (simple parsing - enhance as needed)
        quality_score = self._extract_score(evaluation_text)
        approved = "APPROVED" in evaluation_text.upper()
        
        return quality_score, evaluation_text, approved
    
    def _extract_score(self, text: str) -> float:
        """Extract quality score from evaluation text"""
        
        # Simple extraction - look for score mentioned
        import re
        scores = re.findall(r'\b([0-9]{1,2})\s*(?:out of|/)\s*100\b', text)
        if scores:
            return float(scores[0]) / 100.0
        
        # Default score
        return 0.7
