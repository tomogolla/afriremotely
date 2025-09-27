# applications/serializers.py
from rest_framework import serializers
from .models import JobApplications


class JobApplicationSerializer(serializers.ModelSerializer):
    # You can show extra fields (like job title or applicant username) if needed
    job_title = serializers.CharField(source="job.title", read_only=True)
    applicant_username = serializers.CharField(source="applicant.username", read_only=True)

    class Meta:
        model = JobApplications
        fields = [
            "id",
            "job",                 # ForeignKey → JobPosting (id)
            "job_title",           # Read-only (from JobPosting)
            "applicant",           # ForeignKey → User (id)
            "applicant_username",  # Read-only (from User)
            "resume_link",
            "cover_letter",
            "status",
            "applied_at",
            "updated_at",
        ]
        read_only_fields = ["status", "applied_at", "updated_at"]
