# API Endpoints Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "app": "College Major RAG System",
  "version": "0.1.0"
}
```

---

### 2. Get Recommendations
**POST** `/recommendations`

Get personalized course and career recommendations for a student.

**Request Body:**
```json
{
  "query": "What courses should I take to become a machine learning engineer?",
  "major": "Computer Science",
  "academic_year": 2,
  "gpa": 3.8,
  "interests": ["AI", "Data Science", "Software Engineering"],
  "career_goals": "Work at a tech company on ML systems"
}
```

**Parameters:**
- `query` (string, required): The student's question or request
- `major` (string, required): Student's major
- `academic_year` (integer, required): Current year (1-4)
- `gpa` (float, optional): Student's GPA
- `interests` (array of strings, optional): Areas of interest
- `career_goals` (string, optional): Desired career path

**Response (200 OK):**
```json
{
  "query_id": "550e8400-e29b-41d4-a716-446655440000",
  "student_major": "Computer Science",
  "recommended_courses": [
    {
      "course_id": "CS301",
      "course_name": "Machine Learning",
      "semester": 1,
      "reason": "Directly relevant to your ML career goals",
      "difficulty": "intermediate"
    },
    {
      "course_id": "MATH201",
      "course_name": "Linear Algebra",
      "semester": 1,
      "reason": "Essential mathematical foundation for ML",
      "difficulty": "intermediate"
    }
  ],
  "skills_to_develop": [
    "Python programming",
    "Statistics and probability",
    "Linear algebra",
    "Data preprocessing",
    "Model evaluation"
  ],
  "resources": [
    {
      "title": "Deep Learning Specialization",
      "description": "Comprehensive deep learning course by Andrew Ng",
      "type": "course",
      "url": "https://coursera.org/specializations/deep-learning"
    },
    {
      "title": "Python for Data Science Handbook",
      "description": "Practical guide to data science with Python",
      "type": "book"
    }
  ],
  "action_plan": "Start with foundational ML courses this semester, then progress to advanced topics. Build projects to solidify knowledge.",
  "next_steps": [
    "Enroll in CS301 Machine Learning",
    "Complete linear algebra prerequisite",
    "Start Deep Learning Specialization on Coursera",
    "Join AI/ML student club"
  ],
  "mentorship_opportunities": [
    "Connect with alumni working in ML at top tech companies",
    "Find faculty mentor for research project"
  ],
  "quality_score": 0.95
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

### 3. Root
**GET** `/`

Get API information.

**Response:**
```json
{
  "message": "College Major RAG System API",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Interactive API Documentation

### Swagger UI
Visit `http://localhost:8000/docs` to access the interactive Swagger UI documentation where you can test endpoints directly.

### ReDoc
Visit `http://localhost:8000/redoc` for alternative API documentation.

---

## Error Handling

All error responses follow this format:

```json
{
  "detail": "Error description"
}
```

**Common Status Codes:**
- `200` - OK: Request successful
- `400` - Bad Request: Invalid parameters
- `500` - Internal Server Error: Server-side error

---

## Rate Limiting

Currently, there are no rate limits, but they may be added in future versions.

---

## Authentication

Authentication will be implemented in a future version.
