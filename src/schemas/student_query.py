"""Student query schema"""

from pydantic import BaseModel
from typing import Optional, List


class StudentQuery(BaseModel):
    """Student query request schema"""
    
    query: str
    major: str
    academic_year: int  # 1-4
    gpa: Optional[float] = None
    interests: Optional[List[str]] = None
    career_goals: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What courses should I take to become a machine learning engineer?",
                "major": "Computer Science",
                "academic_year": 2,
                "gpa": 3.8,
                "interests": ["AI", "Data Science", "Software Engineering"],
                "career_goals": "Work at a tech company on ML systems"
            }
        }
