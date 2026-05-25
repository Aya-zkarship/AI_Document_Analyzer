# analyzer/models.py
from django.db import models

class JobDescription(models.Model):
    title = models.CharField(max_length=255, help_text="Bhal: Python Developer")
    description_text = models.TextField(help_text="L-anonce d lkhdma kamla")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ResumeAnalysis(models.Model):
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="analyses")
    resume_file = models.FileField(upload_to="resumes/")
    extracted_text = models.TextField(blank=True, null=True)
    ai_result = models.JSONField(blank=True, null=True) 
    match_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for Job {self.job_description.title} - Score: {self.match_percentage}%"
