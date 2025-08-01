Career Skill Quest
Career Skill Quest is an AI-powered platform designed to help users assess their skills, identify knowledge gaps, and receive tailored job recommendations. The application analyzes a user's resume data, generates a custom skill assessment test, provides detailed feedback, suggests learning resources, and recommends suitable job postings.

The backend is built with FastAPI and Python, utilizing the Gemini AI model for generating dynamic content. The frontend is a simple, single-page application built with HTML, CSS, and JavaScript.

Features
Resume Analysis: Users can manually input their resume details, including experience, education, and skills.

Skill Assessment Test: The application generates a multiple-choice skill test based on the user's provided skills and experience level.

AI-Powered Feedback: After the test, the system provides detailed feedback, highlighting strengths and weaknesses.

Personalized Learning Paths: Based on test results, the application suggests specific learning paths and resources to improve identified weaknesses.

Job Recommendations: Using the user's profile and skills, the platform recommends relevant job postings.

Prerequisites
To run this project, you will need the following installed:

Python 3.8+

uv: A fast Python package installer and virtual environment manager.

Installation
This project uses uv for package management. Follow these steps to get the project running on your local machine.

Clone the repository:

git clone <repository_url>
cd career-skill-quest

Create a virtual environment with uv:

uv venv
source .venv/bin/activate

Install dependencies:

uv pip install -r requirements.txt

Set up API Keys:
The project requires API keys for both Google Gemini and SerpApi to function correctly.

Create a .env file in the root directory of the project.

Add your API keys to the file in the following format:

GOOGLE_API_KEY="your_google_api_key"
SERPAPI_API_KEY="your_serpapi_api_key"

Running the Application
After installation, you can run the FastAPI server to start the application.

Start the server using uvicorn:

uvicorn main:app --reload

Access the application:
Open your web browser and navigate to http://127.0.0.1:8000.

Project Structure
main.py: The FastAPI application entry point, defining the API endpoints for resume parsing, test generation, and job recommendations.

services/: A directory containing the core business logic.

gemini_service.py: Handles interactions with the Gemini AI model.

job_recommender.py: Fetches and recommends job postings.

test_generator.py: Creates skill assessment tests and evaluates submissions.

models/: Contains Pydantic models for data validation and structure.

static/: Stores static assets like the style.css file.

templates/: Stores HTML templates, including the main index.html.

Dependencies
The key Python packages used in this project are:

fastapi: A modern, fast web framework for building APIs.

pydantic: For data validation.

uvicorn: An ASGI server for running the FastAPI application.

python-dotenv: To manage environment variables.

langchain-google-genai: To integrate with the Gemini API.

serpapi: To fetch real-time job posting data.