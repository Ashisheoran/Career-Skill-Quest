# pydantic_models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ResumeData(BaseModel):
    name: str = Field(..., description="Extracted name from the resume.")
    email: str = Field(..., description="Extracted email from the resume.")
    experience: str = Field(..., description="Extracted experience summary from the resume.")
    experience_years: int = Field(..., description="Estimated years of experience.")
    education: str = Field(..., description="Extracted education summary from the resume.")
    skills: List[str] = Field(..., description="List of extracted skills.")

class TestQuestion(BaseModel):
    question: str = Field(..., description="The question text.")
    options: Optional[List[str]] = Field(None, description="List of options for MCQ, if applicable.")
    correct_answer: Optional[str] = Field(None, description="Correct answer for MCQ, if applicable.")
    code_template: Optional[str] = Field(None, description="Code template for coding questions, if applicable.")
    expected_output_example: Optional[str] = Field(None, description="Example output for coding/short answer questions.")

class SkillTestRequest(BaseModel):
    skills: List[str] = Field(..., description="List of skills to generate questions for.")
    experience_years: int = Field(5, description="Years of experience for difficulty adjustment.")
    num_questions: int = Field(5, description="Number of questions to generate.")
    question_type: str = Field("mcq", description="Type of questions: 'mcq' or 'coding'.")

class TestSubmission(BaseModel):
    questions: List[TestQuestion] = Field(..., description="The list of questions presented to the user.")
    answers: Dict[str, str] = Field(..., description="A dictionary of user answers, keyed by question index.")

class LearningResource(BaseModel):
    title: str = Field(..., description="Title of the learning resource.")
    link: str = Field(..., description="URL link to the learning resource.")
    description: str = Field(..., description="Brief description of the resource.")

class LearningPath(BaseModel):
    topic: str = Field(..., description="The specific topic or weakness this path addresses.")
    reason: str = Field(..., description="Why this learning path is recommended (e.g., area of weakness).")
    path: str = Field(..., description="A suggested learning path or steps for this topic.")
    resources: List[LearningResource] = Field(..., description="List of specific resources for this learning path.")


class TestResult(BaseModel):
    overall_feedback: str = Field(..., description="General feedback on the test performance.")
    strengths: List[str] = Field(..., description="List of identified strengths.")
    weaknesses: List[str] = Field(..., description="List of identified weaknesses.")
    detailed_feedback: List[str] = Field(..., description="Question-by-question feedback.")
    general_learning_resources: List[LearningResource] = Field(..., description="General resources for improvement.")
    specific_learning_paths: List[LearningPath] = Field(..., description="Specific, structured learning paths for weaknesses.")

class JobPosting(BaseModel):
    id: str = Field(..., description="Unique identifier for the job posting.")
    title: str = Field(..., description="Job title.")
    company: str = Field(..., description="Company name.")
    location: str = Field(..., description="Job location.")
    description: str = Field(..., description="Full job description or a summary.")
    apply_link: str = Field(..., description="Direct link to apply for the job.")