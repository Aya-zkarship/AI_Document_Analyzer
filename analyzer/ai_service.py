# analyzer/ai_service.py
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

def analyze_resume_with_ai(resume_text, job_description):
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"error": "GROQ_API_KEY is missing from your .env file"}
        
    client = Groq(api_key=api_key)
    
    # Upgradina l-prompt bach y-kon strictly formatting block forced
    prompt = f"""
    You are an expert technical recruiter. Analyze the Resume against the Job Description.
    Return your response ONLY as a JSON object inside a ```json ``` markdown block. No other text.

    Required JSON Structure:
    {{
        "match_percentage": 75,
        "matched_skills": ["Skill1", "Skill2"],
        "missing_skills": ["Skill3", "Skill4"],
        "feedback": "Write a short professional advice sentence."
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.1,
        )
        
        response_content = chat_completion.choices[0].message.content.strip()
        
        # Regex powerful helper: kay-jbed ghir l-block li mktoub dakhil JSON brackets {} hta ila l-AI bda kay-khwwer
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if json_match:
            clean_json_text = json_match.group(0)
            return json.loads(clean_json_text)
            
        return json.loads(response_content)
        
    except (json.JSONDecodeError, Exception) as e:
        # Fallback block dynamic b dynamic score helper ghir bach tchofi dynamic logic
        return {
            "match_percentage": 25, 
            "matched_skills": ["Python (Default)"],
            "missing_skills": ["Check inputs"],
            "feedback": f"Format issue or input text too short. API raw: {str(e)}"
        }