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
    
    # Strict prompt setup without field conflicts
    prompt = f"""
You are an advanced Applicant Tracking System (ATS) core analyzer. 
Evaluate the candidate's Resume against the Job Description with strict technical alignment rules.

Calculate the match score precisely based on:
- Hard Skills Match (60% weight)
- Tools & Frameworks Match (30% weight)
- Experience Level Match (10% weight)

You must respond strictly with a valid JSON object. No conversational fillers, no markdown block wrappers (like ```json).

Strict JSON Output Format Required:
{{
    "match_percentage": 75,
    "matched_skills": ["Django", "Python"],
    "missing_skills": ["Docker", "PostgreSQL"],
    "feedback": "Your professional feedback sentence here."
}}

Resume Text:
{resume_text}

Job Description Text:
{job_description}
"""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            # ✅ Bddli had line s s-smiya l-jdida stable
            model="llama-3.3-70b-versatile", 
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        
        response_content = chat_completion.choices[0].message.content.strip()
        
        # Safe extraction check
        json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
            
        return json.loads(response_content)
        
    except (json.JSONDecodeError, Exception) as e:
        return {
            "match_percentage": 0, 
            "matched_skills": [],
            "missing_skills": [],
            "feedback": f"Parsing failure or empty input. Technical error: {str(e)}"
        }