from rest_framework import serializers
from jobs.models import JobPosting, Category, Location
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'country']

class JobPostingSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    posted_by = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'description', 'company_name', 'employment_type', 
            'location', 'category', 'posted_by', 'created_at', 'updated_at',
            'work_mode', 'experience_level', 'salary', 'responsibilities', 
            'professional_skills', 'tags'
            ]

            
class JobPostingListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'company_name', 'employment_type', 'location', 
                  'category', 'work_mode', 'experience_level', 'salary', 'created_at']