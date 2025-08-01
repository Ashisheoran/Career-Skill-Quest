import re
from services.gemini_service import GeminiService
from models.pydantic_models import TestQuestion, TestResult, LearningPath, LearningResource
from typing import List, Dict, Any
import json

class TestGenerator:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def generate_test(
        self, skills: List[str], experience_years: int, num_questions: int = 5, question_type: str = "mcq"
    ) -> List[TestQuestion]:
        """
        Generates a skill assessment test based on provided skills and experience.
        """
        if not skills:
            return []
        difficulty = "beginner"
        if experience_years >= 5:
            difficulty = "advanced"
        elif experience_years >= 2:
            difficulty = "intermediate"

        skills_str = ", ".join(skills)

        if question_type == "mcq":

            prompt = (
                f"As an experienced technical interviewer and assessment creator, generate {num_questions} multiple-choice questions (MCQs) for a skill assessment test.\n"
                f"The questions should rigorously test the candidate's understanding of the following skills: {skills_str}.\n"
                f"The difficulty level for these questions must be strictly {difficulty}. Ensure questions are challenging but fair for this level.\n"
                f"Each question must have exactly 4 distinct options (A, B, C, D), and only one correct answer. Options should be plausible but clearly distinguishable.\n"
                f"Ensure the questions are diverse and cover different aspects or sub-topics within the provided skills, rather than focusing on a single narrow area.\n"
                f"Format the entire output as a single JSON array of objects. Each object must strictly adhere to the following structure:\n"
                f"{{\n"
                f"  \"question\": \"[Your question text here]\",\n"
                f"  \"options\": [\"A. Option 1\", \"B. Option 2\", \"C. Option 3\", \"D. Option 4\"],\n"
                f"  \"correct_answer\": \"[Correct option letter, e.g., 'A']\"\n"
                f"}}\n"
                f"Example format for a single object: [\n"
                f"  {{\n"
                f"    \"question\": \"What is Python's Global Interpreter Lock (GIL)?\",\n"
                f"    \"options\": [\"A. A mechanism that ensures only one thread executes Python bytecode at a time\", \"B. A security feature to prevent unauthorized code execution\", \"C. A garbage collection algorithm\", \"D. A tool for concurrent programming\"],\n"
                f"    \"correct_answer\": \"A\"\n"
                f"  }}\n"
                f"]\n"
                f"Do not include any conversational text, explanations, or extraneous characters outside the JSON array."
            )
            schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "string"}, "minItems": 4, "maxItems": 4},
                        "correct_answer": {"type": "string", "pattern": "^[A-D]$"}
                    },
                    "required": ["question", "options", "correct_answer"]
                }
            }
        elif question_type == "coding":
 
            prompt = (
                f"As a senior software engineer and technical challenge designer, create {num_questions} coding challenge questions for a skill assessment test.\n"
                f"The challenges should primarily focus on testing the candidate's practical application of the following skills: {skills_str}.\n"
                f"The difficulty level of these coding challenges must be strictly {difficulty}. The problems should be solvable within a reasonable time by a candidate at this experience level.\n"
                f"For each question, provide a concise and clear problem description, at least one concrete input/output example to illustrate the expected behavior, and an optional, basic function signature or code template to get them started.\n"
                f"Ensure the coding questions are diverse in their approach and cover common algorithms, data structures, or practical programming paradigms relevant to the skills.\n"
                f"Format the entire output as a single JSON array of objects. Each object must strictly adhere to the following structure:\n"
                f"{{\n"
                f"  \"question\": \"[Problem description here]\",\n"
                f"  \"code_template\": \"[Optional: Function signature or basic code snippet]\",\n"
                f"  \"expected_output_example\": \"[Input example] -> [Expected output example]\"\n"
                f"}}\n"
                f"Example format for a single object: [\n"
                f"  {{\n"
                f"    \"question\": \"Write a Python function that takes a list of integers and returns a new list with only the even numbers.\",\n"
                f"    \"code_template\": \"def filter_evens(numbers):\\n  # Your code here\\n  pass\",\n"
                f"    \"expected_output_example\": \"filter_evens([1, 2, 3, 4, 5, 6]) -> [2, 4, 6]\"\n"
                f"  }}\n"
                f"]\n"
                f"Do not include any conversational text, explanations, or extraneous characters outside the JSON array."
            )
            schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "code_template": {"type": "string"},
                        "expected_output_example": {"type": "string"}
                    },
                    "required": ["question"] 
                }
            }
        else:
            raise ValueError("Unsupported question type. Choose 'mcq' or 'coding'.")

        try:
            raw_questions = await self.gemini_service.generate_structured_response(prompt, schema)
            questions = [TestQuestion(**q) for q in raw_questions]
            return questions
        except Exception as e:
            print(f"Failed to generate test questions: {e}")
            raise

    async def evaluate_test(
        self, questions: List[TestQuestion], answers: Dict[str, str]
    ) -> TestResult:
        """
        Evaluates test answers and provides feedback, strengths, weaknesses,
        and learning resources using Gemini.
        Now includes specific learning paths for weaknesses.
        """
        evaluation_prompt_parts = [
            "As an empathetic, insightful, and highly skilled technical interviewer and career coach, "
            "evaluate the following test submission comprehensively. Your goal is to provide constructive "
            "and actionable feedback, highlighting both strengths and areas for improvement, and suggesting "
            "clear paths for learning and growth. Aim for a supportive and encouraging tone.\n\n"
            "--- Candidate Test Submission Details ---\n"
        ]
        correct_count = 0
        total_count = len(questions)
        feedback_details = []
        weakness_topics = set() 

        for i, q in enumerate(questions):
            question_id = str(i)
            user_answer = answers.get(question_id, "No answer provided.")

            evaluation_prompt_parts.append(f"Question {i+1}:\n")
            evaluation_prompt_parts.append(f"  Question Text: {q.question}\n")

            if q.options: # MCQ
                evaluation_prompt_parts.append(f"  Options: {', '.join(q.options)}\n")
                evaluation_prompt_parts.append(f"  Correct Answer: {q.correct_answer}\n")
                evaluation_prompt_parts.append(f"  User's Answer: {user_answer}\n")
                
                # check for correctness
                is_correct = user_answer.strip().lower() == q.correct_answer.strip().lower()
                if is_correct:
                    correct_count += 1
                    feedback_details.append(f"Question {i+1} (MCQ): Correct. Good understanding.")
                else:
                    feedback_details.append(f"Question {i+1} (MCQ): Incorrect. User answered '{user_answer}', correct was '{q.correct_answer}'. Review this topic.")
                    # Extract a topic from the question for weakness
                    topic_match = re.search(r"What is (.*?)\?|Explain (.*?)|Describe (.*?)|How does (.*?) work", q.question, re.IGNORECASE)
                    topic = topic_match.group(1) or topic_match.group(2) or topic_match.group(3) or topic_match.group(4) if topic_match else q.question.split(' ')[0]
                    if topic: 
                         weakness_topics.add(topic.strip())

            else: # Coding/Short Answer
                evaluation_prompt_parts.append(f"  User's Submission:\n```\n{user_answer}\n```\n")
                if q.expected_output_example:
                    evaluation_prompt_parts.append(f"  Expected Output Example: {q.expected_output_example}\n")
                
                # For coding questions, we can't auto-grade. We need the LLM to provide feedback.
                # Indicate to the LLM that this is a coding question and requires more detailed analysis.
                evaluation_prompt_parts.append(f"  (This is a coding/open-ended question. Please provide detailed feedback on the logic, correctness, and best practices. Identify key areas for improvement or commend strong solutions.)\n")
                
                # Add question text to weakness topics if specific feedback points to a gap
                topic_match = re.search(r"Write a (.*?) function|Implement (.*?)|Solve (.*?) problem", q.question, re.IGNORECASE)
                topic = topic_match.group(1) or topic_match.group(2) or topic_match.group(3) if topic_match else q.question.split(' ')[0]
                if topic: 
                    weakness_topics.add(topic.strip())


            evaluation_prompt_parts.append("\n") 

        evaluation_prompt_parts.append(f"--- End of Submission ---\n\n")
        evaluation_prompt_parts.append(f"Based on the above submission, provide the following in a structured JSON format:\n")
        evaluation_prompt_parts.append(f"1.  **overall_feedback**: A concise summary (2-3 sentences) of the candidate's performance.\n")
        evaluation_prompt_parts.append(f"2.  **strengths**: A bulleted list of 2-4 key skills or areas where the candidate performed well.\n")
        evaluation_prompt_parts.append(f"3.  **weaknesses**: A bulleted list of 2-4 key skills or areas where the candidate needs significant improvement. Be specific.\n")
        evaluation_prompt_parts.append(f"4.  **detailed_feedback**: A question-by-question breakdown, offering specific insights, corrections, or alternative solutions. For coding questions, analyze code logic, efficiency, and correctness.\n")
        evaluation_prompt_parts.append(f"5.  **general_learning_resources**: A list of 2-3 broad learning resources (e.g., platforms, books, concepts) relevant to overall skill development. Include title, link, and a brief description.\n")
        evaluation_prompt_parts.append(f"6.  **specific_learning_paths**: A list of 2-3 highly specific learning paths, each tied directly to an identified weakness. For each path, include:\n")
        evaluation_prompt_parts.append(f"    -   `topic`: The specific skill/concept for this path (e.g., 'Python Decorators', 'SQL Joins').\n")
        evaluation_prompt_parts.append(f"    -   `reason`: Why this path is recommended (e.g., 'Lack of understanding in X', 'Errors in applying Y').\n")
        evaluation_prompt_parts.append(f"    -   `path`: 2-3 actionable steps or a mini-curriculum for learning this topic.\n")
        evaluation_prompt_parts.append(f"    -   `resources`: 2-3 highly relevant, direct links to tutorials, documentation, or courses for *this specific topic*. Provide title, link, and description for each.\n\n")

        evaluation_prompt_parts.append(f"Ensure the JSON output strictly follows the `TestResult` Pydantic model structure, including all nested objects and arrays. Your response should contain ONLY the JSON.\n")
        
        schema = {
            "type": "object",
            "properties": {
                "overall_feedback": {"type": "string"},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "weaknesses": {"type": "array", "items": {"type": "string"}},
                "detailed_feedback": {"type": "array", "items": {"type": "string"}},
                "general_learning_resources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "link": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["title", "link", "description"]
                    }
                },
                "specific_learning_paths": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"},
                            "reason": {"type": "string"},
                            "path": {"type": "string"},
                            "resources": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "link": {"type": "string"},
                                        "description": {"type": "string"}
                                    },
                                    "required": ["title", "link", "description"]
                                }
                            }
                        },
                        "required": ["topic", "reason", "path", "resources"]
                    }
                }
            },
            "required": [
                "overall_feedback",
                "strengths",
                "weaknesses",
                "detailed_feedback",
                "general_learning_resources",
                "specific_learning_paths"
            ]
        }

        full_prompt = "".join(evaluation_prompt_parts)

        try:
            raw_results = await self.gemini_service.generate_structured_response(full_prompt, schema)

            if not isinstance(raw_results, dict):
                try:
                    raw_results = json.loads(raw_results)
                except json.JSONDecodeError:
                    raise ValueError(f"Gemini response was not a valid JSON dictionary: {raw_results}")
            
            
            if not raw_results.get("strengths"):
                raw_results["strengths"] = [f"Answered {correct_count} out of {total_count} questions correctly."]
            
            if not raw_results.get("weaknesses") and weakness_topics:
                 raw_results["weaknesses"] = list(weakness_topics)
            elif not raw_results.get("weaknesses"):
                 raw_results["weaknesses"] = ["Further review of core concepts is recommended."]

            test_result = TestResult(**raw_results)
            return test_result
        except Exception as e:
            print(f"Failed to evaluate test or parse Gemini response: {e}")
            raise   
