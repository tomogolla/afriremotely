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
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full-time'
        PART_TIME = 'part_time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'

    class WorkMode(models.TextChoices):
        REMOTE = 'remote', 'Remote'
        HYBRID = 'hybrid', 'Hybrid'
        ON_SITE = 'on_site', 'On-site'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'entry', 'Entry'
        MID = 'mid', 'Mid'
        SENIOR = 'senior', 'Senior'
        LEAD = 'lead', 'Lead'


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs")

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs', limit_choices_to={'role': 'recruiter'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    work_mode = models.CharField(max_length=10, choices=WorkMode.choices, default="onsite")
    experience_level = models.CharField(max_length=10, choices=ExperienceLevel.choices, default="entry")
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    responsibilities = models.TextField(blank=True, null=True)
    professional_skills = models.TextField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}, at {self.company_name}"
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]