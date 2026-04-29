"""Recommendation schema"""

from pydantic import BaseModel
from typing import List, Optional


class Resource(BaseModel):
    """Resource recommendation"""
    
    title: str
    description: str
    type: str  # book, course, certification, mentor
    url: Optional[str] = None


class CourseRecommendation(BaseModel):
    """Course recommendation"""
    
    course_id: str
    course_name: str
    semester: int
    reason: str
    difficulty: str  # beginner, intermediate, advanced


class Recommendation(BaseModel):
    """Individual recommendation"""
    
    type: str  # course, skill, resource
    title: str
    description: str
    priority: str  # high, medium, low
    timeline: str


class RecommendationResponse(BaseModel):
    """Full recommendation response"""
    
    query_id: str
    student_major: str
    recommended_courses: List[CourseRecommendation]
    skills_to_develop: List[str]
    resources: List[Resource]
    action_plan: str
    next_steps: List[str]
    mentorship_opportunities: List[str]
    quality_score: float  # 0-1
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "q123",
                "student_major": "Computer Science",
                "recommended_courses": [
                    {
                        "course_id": "CS401",
                        "course_name": "Machine Learning",
                        "semester": 1,
                        "reason": "Directly relevant to your ML career goals",
                        "difficulty": "intermediate"
                    }
                ],
                "skills_to_develop": ["Python", "Statistics", "Linear Algebra"],
                "resources": [
                    {
                        "title": "Deep Learning Specialization",
                        "description": "Comprehensive deep learning course",
                        "type": "course",
                        "url": "https://..."
                    }
                ],
                "action_plan": "Complete core ML courses in first year...",
                "next_steps": ["Enroll in CS401", "Start Python refresher course"],
                "mentorship_opportunities": ["Connect with alumni in ML"],
                "quality_score": 0.95
            }
        }
