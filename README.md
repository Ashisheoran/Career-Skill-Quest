# Career Skill Quest

Career Skill Quest is a modern, AI-powered platform designed to help users advance their careers by assessing skills, identifying knowledge gaps, and receiving personalized job recommendations. The platform leverages the Gemini AI model to analyze user resumes, generate tailored skill tests, provide detailed feedback, and suggest actionable learning paths and job opportunities.

---

## 🚀 Features

- **Resume Analysis:** Users input their skills, experience, and education for in-depth AI-driven analysis.
- **Skill Assessment:** Generates adaptive, multiple-choice quizzes based on user skills and experience level.
- **AI Feedback:** Delivers detailed, personalized insights into strengths and areas for growth.
- **Personalized Learning Paths:** Recommends specific resources and learning plans to address skill gaps.
- **Job Recommendations:** Uses real-time data to match users with relevant job postings.
- **Modern, Responsive UI:** Clean and accessible interface with progress tracking and step-by-step forms

---

## View ScreenShots of Project 

[View the images directory](https://github.com/Ashisheoran/Career-Skill-Quest/tree/main/images)


---

## 🛠️ Tech Stack

- **Environment Management:** [uv](https://github.com/astral-sh/uv) (Python virtual environments and package management)

### Backend
- **Python 3** (core logic & APIs)
- **Pydantic** (data models)
- **FastAPI** 
- **LangChain, Gemini API** (AI/LLM integration via langchain-google-genai)
- **Job Search:** SerpApi
- **[PyMuPDF](https://pymupdf.readthedocs.io/), python-docx** (resume parsing)

### Frontend
- **HTML**
- **CSS**
- **JavaScript** (Single-Page Application)

---

## 🗂️ Project Structure

```
Career-Skill-Quest/
│
├── main.py               # FastAPI entry point for backend API
├── requirements.txt      # Python dependencies
├── .env                  # Environment secrets (not tracked in Git)
│
├── services/             # Core backend modules
│   ├── gemini_service.py     # Gemini AI integration logic
│   ├── job_recommender.py    # Job recommendation engine
│   └── test_generator.py     # Skill test generation & evaluation
│
├── models/               # Pydantic models for data validation
│
├── static/               # Static frontend files
│   ├── app.js                # Main JavaScript for SPA
│   ├── style.css             # Main CSS
│   └── ...                   # Other static assets
│
├── templates/            # HTML templates (Single-Page Application)
│   ├── index.html            # Main frontend template
│   └── ...                   # Other HTML files (if any)
│
├── images/               # Project screenshots and visuals
├── README.md             # Project documentation
└── LICENSE               # Project license (MIT)
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
   uv init
   uv venv
   .venv/Scripts/activate
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

## ✨ Contributing

Contributions, issues, and feature requests are welcome!  
Please open an issue or submit a pull request.

1. Fork the repo and create your branch:
   ```
   git checkout -b feature/your-feature
   ```
2. Commit your changes and push:
   ```
   git commit -m "Describe your change"
   git push origin feature/your-feature
   ```
3. Open a Pull Request on GitHub.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). 

---
## Created By

[Ashish Sheoran](https://github.com/Ashisheoran)

---

## 👏 Acknowledgements

- Python, Pydantic, LangChain, SerpApi, Google Gemini, PyMuPDF, and the open source community.

---
**Empowering your career with AI-driven insights, assessments, and opportunities!**

> *Explore, learn, and achieve your career goals with Career Skill Quest!*

---

*Note: For the full file and feature set, explore the [GitHub repository](https://github.com/Ashisheoran/Career-Skill-Quest).*
