# Career Skill Quest

Career Skill Quest is a modern, AI-powered platform designed to help users advance their careers by assessing skills, identifying knowledge gaps, and receiving personalized job recommendations. The platform leverages the Gemini AI model to analyze user resumes, generate tailored skill tests, provide detailed feedback, and suggest actionable learning paths and job opportunities.

---

## 🚀 Features

- **Resume Analysis:** Users input their skills, experience, and education for in-depth AI-driven analysis.
- **Skill Assessment:** Generates adaptive, multiple-choice quizzes based on user skills and experience level.
- **AI Feedback:** Delivers detailed, personalized insights into strengths and areas for growth.
- **Personalized Learning Paths:** Recommends specific resources and learning plans to address skill gaps.
- **Job Recommendations:** Uses real-time data to match users with relevant job postings.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Gemini AI (via langchain-google-genai)
- **Frontend:** HTML, CSS, JavaScript (Single-Page Application)
- **Job Data:** SerpApi
- **Environment Management:** [uv](https://github.com/astral-sh/uv) (Python virtual environments and package management)

---

## ⚡ Getting Started

### Prerequisites

- Python 3.8 or newer
- [uv](https://github.com/astral-sh/uv) installed

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Ashisheoran/Career-Skill-Quest.git
   cd Career-Skill-Quest
   ```

2. **Create and activate a virtual environment:**
   ```sh
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   uv pip install -r requirements.txt
   uv sync    # if pyproject.toml exist
   ```

4. **Set up API keys:**
   - Create a `.env` file in the root directory.
   - Add your keys:
     ```
     GOOGLE_API_KEY="your_google_api_key"
     SERPAPI_API_KEY="your_serpapi_api_key"
     ```

---

## ▶️ Running the Application

Start the FastAPI server with Uvicorn:

```sh
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🗂️ Project Structure

```
Career-Skill-Quest/
│
├── main.py               # FastAPI entry point
├── requirements.txt      # Python dependencies
├── services/             # Core logic modules
│   ├── gemini_service.py     # Gemini AI integration
│   ├── job_recommender.py    # Job recommendation logic
│   └── test_generator.py     # Skill test generation & evaluation
├── models/               # Pydantic models for data validation
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates (SPA)
└── .env                  # Your API keys (not tracked)
```

---

## 🧩 Key Dependencies

- `fastapi` – Lightning-fast API development
- `pydantic` – Data validation and parsing
- `uvicorn` – ASGI server for FastAPI
- `python-dotenv` – Environment variable management
- `langchain-google-genai` – Gemini AI integration
- `serpapi` – Real-time job data fetching

---

## ✨ Contributing

Contributions, issues, and feature requests are welcome!  
Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). 
@Ashisheoran

---

**Empowering your career with AI-driven insights, assessments, and opportunities!**
