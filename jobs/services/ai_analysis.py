from openai import OpenAI
from django.conf import settings
import json
from google.genai.errors import ServerError


client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a software engineering career coach. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        raise Exception(
            "The AI service is temporarily busy. Please try again in a few minutes."
        )