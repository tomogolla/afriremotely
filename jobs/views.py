from django.shortcuts import render

# jobs/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import JobPosting
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

@api_view(["GET"])
def job_choices(request):
    data = {
        "employment_types": dict(JobPosting.EMPLOYMENT_TYPES),
        "work_modes": dict(JobPosting.WORK_MODES),
        "experience_levels": dict(JobPosting.EXPERIENCE_LEVELS),
    }
    return Response(data)




class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def home_view(request):
    return render(request, 'home.html')
