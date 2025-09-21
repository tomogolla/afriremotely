from django.contrib import admin
from .models import User, ApplicantProfile, RecruiterProfile

admin.site.register(User)
admin.site.register(ApplicantProfile)
admin.site.register(RecruiterProfile)
