from django.db import models
import uuid
from users.models import User

# category

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

# location

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.country}"
    

# jobposting

class JobPosting(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]

    WORK_MODE_CHOICES = [
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
        ("onsite", "On-site"),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ("entry", "Entry"),
        ("mid", "Mid"),
        ("senior", "Senior"),
        ("lead", "Lead"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs")

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs', limit_choices_to={'role': 'recruiter'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES, default="onsite")
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES, default="entry")
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    responsibilities = models.TextField(blank=True, null=True)
    professional_skills = models.TextField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}, at {self.company_name}"