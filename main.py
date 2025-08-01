# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv()

# --- Project Imports ---
from services.gemini_service import GeminiService
from services.test_generator import TestGenerator
from services.job_recommender import JobRecommender
from models.pydantic_models import (
    ResumeData, SkillTestRequest, TestQuestion, TestSubmission,
    TestResult, JobPosting
)

# --- FastAPI App Setup ---
app = FastAPI(
    title="AI-Powered Resume Analyzer & Skill Assessment Platform",
    description="Analyze manually entered resume details, generate skill tests, provide feedback, and recommend jobs using Gemini AI."
)

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# --- Initialize Services ---
# Ensure GOOGLE_API_KEY is set in your .env file
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file.")

serpapi_api_key = os.getenv("SERPAPI_API_KEY")
if not serpapi_api_key:
    raise ValueError("SERPAPI_API_KEY environment variable not set. Please set it in your .env file.")

gemini_service = GeminiService(api_key=google_api_key)
test_generator = TestGenerator(gemini_service=gemini_service)
job_recommender = JobRecommender(gemini_service=gemini_service, serpapi_api_key=serpapi_api_key)

# --- Routes ---

@app.get("/", response_class=HTMLResponse, summary="Home Page")
async def read_root(request: Request):
    """
    Serves the main HTML page for the application.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-resume-details", response_model=ResumeData, summary="Submit Manual Resume Details")
async def submit_manual_resume_details(resume_data: ResumeData):
    """
    Accepts manually entered resume details and returns them.
    This acts as the "parsing" step for manual input.
    """
    return resume_data

@app.post("/generate-test", response_model=List[TestQuestion], summary="Generate Skill Test")
async def generate_skill_test(request_data: SkillTestRequest):
    """
    Generates a skill assessment test (MCQs or coding questions) based on provided skills
    and desired difficulty.
    """
    try:
        test_questions = await test_generator.generate_test(
            skills=request_data.skills,
            experience_years=request_data.experience_years,
            num_questions=request_data.num_questions,
            question_type=request_data.question_type
        )
        return test_questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test: {str(e)}")

@app.post("/evaluate-test", response_model=TestResult, summary="Submit Test and Get Feedback")
async def submit_test_and_get_feedback(submission: TestSubmission):
    """
    Evaluates submitted test answers and provides instant feedback,
    strengths, weaknesses, and learning resources.
    """
    try:
        test_result = await test_generator.evaluate_test(
            questions=submission.questions,
            answers=submission.answers
        )
        return test_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating test: {str(e)}")

@app.post("/recommend-jobs", response_model=List[JobPosting], summary="Recommend Jobs")
async def recommend_jobs(resume_data: ResumeData):
    """
    Recommends suitable job postings based on the candidate's extracted skills and experience.
    This now uses the mock job API to get dynamic jobs.
    """
    try:
        recommendations = await job_recommender.recommend_jobs(
            skills=resume_data.skills,
            experience_years=resume_data.experience_years,
            education=resume_data.education
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommending jobs: {str(e)}")