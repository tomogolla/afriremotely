from rest_framework import serializers
from .models import User, ApplicantProfile, RecruiterProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.get('role')
        user = User.objects.create_user(**validated_data)
        User.save()

        if role == "applicant":
            ApplicantProfile.objects.create(user=user)
        elif role == 'recruiter':
            RecruiterProfile.objects.create(user = user)

            
        return user




class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.DictField(read_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)
        return {
            "username": user.username,
            "role": user.role,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role"] 

class ApplicantProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )
    class Meta:
        model = ApplicantProfile
        fields = [
            "id", 
            "user",
            "user_id",
            "resume",
            "education_level",
            "experience_years",
            "skills",
        ]

# Recruiter Profile Serializer
class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )

    class Meta:
        model = RecruiterProfile
        fields = [
            "id",
            "user",
            "user_id",
            "company_name",
            "company_website",
            "position",
        ]