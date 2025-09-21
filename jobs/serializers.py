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
        field = ['id', 'city', 'country']

class JobPostingSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(read_only=True)
    Location_id = LocationSerializer(read_only=True)
    posted_by = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = JobPosting
        field = [
            'id', 'title', 'description', 'company_name', 'employment_type', 
            'location_id', 'category_id', 'posted_by', 'created_at', 'updated_at',
            'work_mode', 'experience_level', 'salary', 'responsibilities', 
            'professional_skills', 'tags'
            ]

            
class JobPostingListSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer(read_only=True)
    location_id = LocationSerializer(read_only=True)

    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'company_name', 'employment_type', 'location', 
                  'category', 'work_mode', 'experience_level', 'salary', 'created_at']