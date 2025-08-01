# job_recommender.py
import re
from services.gemini_service import GeminiService
from models.pydantic_models import JobPosting
from typing import List, Dict, Any
from serpapi import GoogleSearch
import json # Make sure json is imported here

class JobRecommender:
    def __init__(self, gemini_service: GeminiService, serpapi_api_key: str):
        self.gemini_service = gemini_service
        self.serpapi_api_key = serpapi_api_key

    async def _fetch_real_job_postings(self, query: str, num_jobs: int = 10) -> List[JobPosting]:
        """
        Fetches real job postings using SerpApi based on a query.
        """
        try:
            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": self.serpapi_api_key,
                "location": "India", # Targeting India as per the original mock
                "num": num_jobs # Number of results to fetch
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            
            job_postings = []
            if "jobs_results" in results:
                for idx, job in enumerate(results["jobs_results"]):
                    # Ensure all required fields are present, use default empty string if not
                    title = job.get("title", "N/A")
                    company = job.get("company_name", "N/A")
                    location = job.get("location", "N/A")
                    description = job.get("description", "N/A")
                    apply_link = job.get("job_link", job.get("direct_apply_link", "#")) # Prioritize job_link, then direct_apply_link

                    # SerpApi typically doesn't provide a unique 'id' like a simple number,
                    # so we'll generate one or use a hash of some unique fields if available.
                    # For simplicity, using index here.
                    job_postings.append(
                        JobPosting(
                            id=str(idx + 1),
                            title=title,
                            company=company,
                            location=location,
                            description=description,
                            apply_link=apply_link # Add the apply_link here
                        )
                    )
            return job_postings
        except Exception as e:
            print(f"Error fetching real job postings with SerpApi: {e}")
            return []

    async def recommend_jobs(
        self, skills: List[str], experience_years: int, education: str
    ) -> List[JobPosting]:
        """
        Recommends suitable job postings based on the candidate's profile.
        Now fetches jobs from SerpApi and then performs semantic matching.
        """
        search_query = f"{' '.join(skills)} developer jobs {experience_years} years experience in India"

        # Step 1: Fetch jobs from real API based on a broad query
        fetched_jobs = await self._fetch_real_job_postings(search_query, num_jobs=20) # Fetch more to filter down

        if not fetched_jobs:
            return []

        # Step 2: Use Gemini for semantic matching and filtering
        # Prompt Engineering: Guide the LLM to act as a career advisor and filter the most relevant jobs.
        # Ensure the prompt emphasizes the candidate's profile and job requirements.
        jobs_json_str = json.dumps([job.dict() for job in fetched_jobs]) # Convert Pydantic models to dicts for JSON

        prompt = (
            f"As an expert career advisor and job matching specialist, your task is to review a list of job postings "
            f"and select the top 5-7 most relevant ones for a candidate. "
            f"The candidate's profile is as follows:\n"
            f"Skills: {', '.join(skills)}\n"
            f"Years of Experience: {experience_years}\n"
            f"Education: {education}\n\n"
            f"Here is the list of available job postings in JSON format. Each job includes 'id', 'title', 'company', 'location', 'description', and 'apply_link':\n"
            f"```json\n{jobs_json_str}\n```\n\n"
            f"Please carefully analyze each job description in relation to the candidate's skills, experience, and education. "
            f"Prioritize jobs where the core requirements strongly align with the candidate's profile. "
            f"Return only the selected job postings in a JSON array format, identical to the input `JobPosting` schema. "
            f"Do not include any additional text or explanations, just the JSON array of selected job postings.\n"
            f"If no jobs are highly relevant, return an empty JSON array.\n"
            f"Example of desired output structure:\n"
            f"[\n"
            f"  {{\"id\": \"1\", \"title\": \"Software Engineer\", \"company\": \"Tech Corp\", \"location\": \"Bengaluru\", \"description\": \"Develop scalable software...\", \"apply_link\": \"http://example.com/apply/1\"}}\n"
            f"]"
        )
        
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "location": {"type": "string"},
                    "description": {"type": "string"},
                    "apply_link": {"type": "string"}
                },
                "required": ["id", "title", "company", "location", "description", "apply_link"]
            }
        }

        try:
            # Generate structured response from Gemini based on the prompt and schema
            filtered_jobs_raw = await self.gemini_service.generate_structured_response(prompt, schema)
            
            # Convert raw dicts back to JobPosting models for type safety
            recommended_jobs = [JobPosting(**job_data) for job_data in filtered_jobs_raw]
            return recommended_jobs
        except Exception as e:
            print(f"Error semantically filtering job postings with Gemini: {e}")
            return []