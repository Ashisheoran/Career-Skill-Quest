import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from typing import List, Dict, Any

def clean_json(text: str) -> str:
    text = text.strip()

    # remove markdown fences
    text = re.sub(r"```(?:json)?", "", text)
    text = text.replace("```", "")

    # remove trailing commas
    text = re.sub(r",\s*([}\]])", r"\1", text)

    return text

class GeminiService:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.2  # lower randomness = cleaner JSON
        )
        self.output_parser = StrOutputParser()

    async def generate_text(self, prompt: str) -> str:
        """Generates text using the Gemini model."""
        try:
            response = await self.llm.ainvoke(prompt)
             # Explicitly get the string content from the AIMessage object
            if hasattr(response, 'content'):
                return response.content
            else:
                return self.output_parser.parse(response)
        except Exception as e:
            print(f"Error generating text with Gemini: {e}")
            raise

    async def generate_structured_response(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a structured JSON response using the Gemini model with a given schema.
        Note: LangChain's direct schema enforcement can be tricky. We'll use a prompt to guide the LLM to output JSON and then parse it.
        """
        full_prompt = (
            f"{prompt}\n\n"
            f"Please provide the response in JSON format according to the following schema:\n"
            f"```json\n{json.dumps(schema, indent=2)}\n```\n"
            f"Ensure your response contains ONLY the JSON object/array and no other text or explanations."
        )
        response_content = await self.generate_text(full_prompt)
        json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", response_content, re.DOTALL)
        
        if json_match:
            json_string = json_match.group(1).strip()
        else:
            json_string = response_content.strip()
        
        json_string = clean_json(json_string)
        
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            # retry cleanup once
            json_string = clean_json(json_string)
            return json.loads(json_string)



