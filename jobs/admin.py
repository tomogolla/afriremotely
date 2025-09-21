from django.contrib import admin
from .models import JobPosting, Location, Category

admin.site.register(JobPosting)
admin.site.register(Location)
admin.site.register(Category)
