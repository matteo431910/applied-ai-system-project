"""FastAPI main application"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid

from src.config.settings import settings
from src.schemas.student_query import StudentQuery
from src.schemas.recommendation import RecommendationResponse, CourseRecommendation, Resource
from src.components.retriever import Retriever
from src.components.agent import Agent
from src.components.evaluator import Evaluator
from src.utils.logger import get_logger


logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Retrieval-Augmented Generation system for college major guidance"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG components
retriever = Retriever()
agent = Agent()
evaluator = Evaluator()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }


@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(query: StudentQuery) -> RecommendationResponse:
    """
    Get personalized recommendations for a student
    
    Args:
        query: Student query with context
        
    Returns:
        Personalized recommendations
    """
    try:
        logger.info(f"Processing recommendation request for {query.major}")
        
        # Generate unique ID
        query_id = str(uuid.uuid4())
        
        # Step 1: Retrieve relevant documents
        retrieved_docs = retriever.retrieve(query.query, top_k=5)
        
        # Step 2: Generate recommendations using Agent
        student_context = {
            "major": query.major,
            "academic_year": query.academic_year,
            "gpa": query.gpa,
            "interests": query.interests or [],
            "career_goals": query.career_goals
        }
        
        recommendation_text = agent.process_query(
            query.query,
            student_context,
            retrieved_docs
        )
        
        # Step 3: Evaluate recommendations
        quality_score, feedback, approved = evaluator.evaluate(
            recommendation_text,
            student_context
        )
        
        if not approved:
            logger.warning(f"Recommendation not approved. Feedback: {feedback}")
        
        # Step 4: Format response
        response = RecommendationResponse(
            query_id=query_id,
            student_major=query.major,
            recommended_courses=[
                CourseRecommendation(
                    course_id="CS101",
                    course_name="Introduction to Computer Science",
                    semester=1,
                    reason="Foundation course for your major",
                    difficulty="beginner"
                )
            ],
            skills_to_develop=["Python", "Problem Solving", "Communication"],
            resources=[
                Resource(
                    title="Official Course Materials",
                    description="Course syllabus and lecture notes",
                    type="course"
                )
            ],
            action_plan=recommendation_text[:500],
            next_steps=["Enroll in recommended courses", "Connect with advisors"],
            mentorship_opportunities=["Alumni mentorship program"],
            quality_score=quality_score
        )
        
        logger.info(f"Successfully generated recommendations for query {query_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "College Major RAG System API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
