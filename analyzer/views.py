# analyzer/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import JobDescription, ResumeAnalysis
from .utils import extract_text_from_pdf
from .ai_service import analyze_resume_with_ai

def upload_and_analyze(request):
    if request.method == "POST":
        job_title = request.POST.get("job_title")
        job_text = request.POST.get("job_description")
        resume_file = request.FILES.get("resume")

        if not job_title or not job_text or not resume_file:
            return JsonResponse({"error": "Fields kamlin mandatory!"}, status=400)

        job = JobDescription.objects.create(title=job_title, description_text=job_text)
        
        extracted_text = extract_text_from_pdf(resume_file)
        if not extracted_text:
            return JsonResponse({"error": "Mal9itch text dakhil l-PDF file."}, status=400)

        ai_response = analyze_resume_with_ai(extracted_text, job_text)
        
        # Check security structure logic
        match_score = ai_response.get("match_percentage", 0) if isinstance(ai_response, dict) else 0

        analysis = ResumeAnalysis.objects.create(
            job_description=job,
            resume_file=resume_file,
            extracted_text=extracted_text,
            ai_result=ai_response,
            match_percentage=match_score
        )

        # 🎯 Blast JsonResponse, ghadin n-passiw kollchi l template jdid:
        return render(request, "analyzer/result.html", {
            "analysis": analysis,
            "ai_result": ai_response
        })

    return render(request, "analyzer/upload.html")