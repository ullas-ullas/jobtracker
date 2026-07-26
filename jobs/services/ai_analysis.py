from google import genai
from django.conf import settings
import json
from google.genai.errors import ServerError


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def analyze_job_service(
    title,
    company,
    description,
):

    prompt = f"""
    You are an experienced software engineering career coach.

    Analyze the following job posting for a software developer who is preparing to apply.

    Return:
    1. Summary
    2. Difficulty (Beginner, Intermediate, Advanced)
    3. Required Skills
    4. Interview Questions
    5. Preparation Tips

    Analyze this job posting.

    Job Title:
    {title}

    Company:
    {company}

    Description:
    {description}

    Return ONLY valid JSON.

    {{
    "summary": "",
    "difficulty": "",
    "skills": [],
    "interview_questions": [],
    "preparation_tips": []
    }}

    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.removeprefix("```json").removesuffix("```").strip()

        data =  json.loads(text)
        return data
    except Exception as e:
        raise Exception(
            "The AI service is temporarily busy. Please try again in a few minutes."
        )