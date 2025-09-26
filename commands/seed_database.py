from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, ApplicantProfile, RecruiterProfile
from jobs.models import JobPosting, Category, Location
from applications.models import JobApplications
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with sample data for ProDev Job Board'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Create Categories
        categories_data = [
            {'name': 'Technology', 'description': 'Jobs in software, IT, and tech industries'},
            {'name': 'Healthcare', 'description': 'Medical and healthcare-related roles'},
            {'name': 'Finance', 'description': 'Finance and accounting positions'},
        ]
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} category: {category.name}'))

        # Create Locations
        locations_data = [
            {'city': 'New York', 'country': 'USA'},
            {'city': 'London', 'country': 'UK'},
            {'city': 'Nairobi', 'country': 'Kenya'},
        ]
        locations = []
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(
                city=loc_data['city'], country=loc_data['country']
            )
            locations.append(location)
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} location: {location.city}, {location.country}'))

        # Create Users
        users_data = [
            {
                'username': 'admin1',
                'email': 'admin1@example.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'One',
            },
            {
                'username': 'recruiter1',
                'email': 'recruiter1@example.com',
                'password': 'recruiter123',
                'role': 'recruiter',
                'first_name': 'Recruiter',
                'last_name': 'One',
            },
            {
                'username': 'applicant1',
                'email': 'applicant1@example.com',
                'password': 'applicant123',
                'role': 'applicant',
                'first_name': 'Applicant',
                'last_name': 'One',
            },
            {
                'username': 'applicant2',
                'email': 'applicant2@example.com',
                'password': 'applicant123',
                'role': 'applicant',
                'first_name': 'Applicant',
                'last_name': 'Two',
            },
        ]
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'id': uuid.uuid4(),
                    'username': user_data['username'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'role': user_data['role'],
                    'is_active': True,
                    'created_at': timezone.now(),
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} user: {user.username} ({user.role})'))

        # Create Applicant Profiles
        for user in users:
            if user.role == 'applicant':
                profile, created = ApplicantProfile.objects.get_or_create(
                    id=user,
                    defaults={
                        'resume': 'https://example.com/resumes/sample.pdf',
                        'education_level': 'Bachelor’s Degree',
                        'experience_years': 3,
                        'skills': ['Python', 'Django', 'JavaScript']
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} applicant profile for: {user.username}'))

        # Create Recruiter Profiles
        for user in users:
            if user.role == 'recruiter':
                profile, created = RecruiterProfile.objects.get_or_create(
                    id=user,
                    defaults={
                        'company_name': 'Tech Corp',
                        'company_website': 'https://techcorp.com',
                        'position': 'HR Manager'
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} recruiter profile for: {user.username}'))

        # Create Job Postings
        job_postings_data = [
            {
                'title': 'Senior Python Developer',
                'description': 'Develop scalable backend systems using Python and Django.',
                'company_name': 'Tech Corp',
                'employment_type': 'full_time',
                'location': locations[0],  # New York
                'category': categories[0],  # Technology
                'posted_by': users[1],  # recruiter1
                'work_mode': 'remote',
                'experience_level': 'Senior',
                'salary': 120000.00,
                'responsibilities': 'Design APIs, optimize queries, collaborate with frontend.',
                'professional_skills': 'Python, Django, PostgreSQL',
                'tags': ['backend', 'python', 'remote'],
            },
            {
                'title': 'Nurse Practitioner',
                'description': 'Provide patient care in a hospital setting.',
                'company_name': 'Health Inc',
                'employment_type': 'full_time',
                'location': locations[1],  # London
                'category': categories[1],  # Healthcare
                'posted_by': users[1],  # recruiter1
                'work_mode': 'on_site',
                'experience_level': 'Mid-level',
                'salary': 80000.00,
                'responsibilities': 'Patient assessments, treatment planning.',
                'professional_skills': 'Nursing, Patient Care',
                'tags': ['healthcare', 'nursing'],
            },
        ]
        job_postings = []
        for job_data in job_postings_data:
            job, created = JobPosting.objects.get_or_create(
                title=job_data['title'],
                posted_by=job_data['posted_by'],
                defaults={
                    'description': job_data['description'],
                    'company_name': job_data['company_name'],
                    'employment_type': job_data['employment_type'],
                    'location': job_data['location'],
                    'category': job_data['category'],
                    'work_mode': job_data['work_mode'],
                    'experience_level': job_data['experience_level'],
                    'salary': job_data['salary'],
                    'responsibilities': job_data['responsibilities'],
                    'professional_skills': job_data['professional_skills'],
                    'tags': job_data['tags'],
                    'created_at': timezone.now(),
                }
            )
            job_postings.append(job)
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} job posting: {job.title}'))

        # Create Job Applications
        applications_data = [
            {
                'job_id': job_postings[0],  # Senior Python Developer
                'applicant_id': users[2],  # applicant1
                'resume_link': 'https://example.com/resumes/applicant1.pdf',
                'cover_letter': 'I am excited to apply for this role...',
                'status': 'pending',
            },
            {
                'job_id': job_postings[1],  # Nurse Practitioner
                'applicant_id': users[3],  # applicant2
                'resume_link': 'https://example.com/resumes/applicant2.pdf',
                'cover_letter': 'I have extensive experience in healthcare...',
                'status': 'reviewed',
            },
        ]
        for app_data in applications_data:
            application, created = JobApplications.objects.get_or_create(
                job_id=app_data['job_id'],
                applicant_id=app_data['applicant_id'],
                defaults={
                    'resume_link': app_data['resume_link'],
                    'cover_letter': app_data['cover_letter'],
                    'status': app_data['status'],
                    'applied_at': timezone.now(),
                }
            )
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} application for: {application.job_id.title} by {application.applicant_id.username}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))