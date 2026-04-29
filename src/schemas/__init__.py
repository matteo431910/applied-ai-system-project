"""Data schemas for API requests/responses"""

from .student_query import StudentQuery
from .recommendation import Recommendation, RecommendationResponse

__all__ = ["StudentQuery", "Recommendation", "RecommendationResponse"]
