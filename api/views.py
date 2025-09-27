from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from jobs.models import JobPosting, Category, Location
from jobs.serializers import JobPostingSerializer, JobPostingListSerializer, CategorySerializer, LocationSerializer
from users.models import User, ApplicantProfile, RecruiterProfile
from applications.models import JobApplications
from applications.serializers import JobApplicationSerializer
from users.serializers import UserSerializer


# Custom Permission for Role-Based Access
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['admin', 'recruiter']

class IsAuthenticatedApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'applicant'
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

# JobPosting ViewSet
class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all().select_related('category', 'location', 'posted_by')
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return JobPostingListSerializer
        return JobPostingSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', None)
        location = request.query_params.get('location', None)
        work_mode = request.query_params.get('work_mode', None)

        queryset = self.get_queryset()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(company_name__icontains=query)
            )
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if location:
            queryset = queryset.filter(location__city__iexact=location)
        if work_mode:
            queryset = queryset.filter(work_mode=work_mode)

        serializer = JobPostingListSerializer(queryset, many=True)
        return Response(serializer.data)

# # Category ViewSet
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminOrReadOnly]

# # Location ViewSet
# class LocationViewSet(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer
#     permission_classes = [IsAdminOrReadOnly]



# New action for work_mode choices
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def work_modes(self, request):
        work_modes = [
            {'value': choice[0], 'label': choice[1]}
            for choice in JobPosting.WorkMode.choices
        ]
        return Response(work_modes)

    # New action for employment_type choices
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def employment_types(self, request):
        employment_types = [
            {'value': choice[0], 'label': choice[1]}
            for choice in JobPosting.EmploymentType.choices
        ]
        return Response(employment_types)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def experience_level(self, request):
        experience_levels = [
            {'value': choice[0], 'label': choice[1]}
            for choice in JobPosting.ExperienceLevel.choices
        ]
        return Response(experience_levels)


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    # New action for job types (categories)
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def list_types(self, request):
        categories = self.get_queryset()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# Location ViewSet (unchanged)
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]

# JobApplication ViewSet (unchanged)
class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplications.objects.all().select_related('job_id', 'applicant_id')

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticatedApplicant()]
        if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrReadOnly()]
        if self.action == 'my_applications':
            return [IsAuthenticatedApplicant()]
        return super().get_permissions()

    def get_serializer_class(self):
        return JobApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(applicant_id=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedApplicant])
    def my_applications(self, request):
        queryset = self.get_queryset().filter(applicant_id=request.user)
        status = request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        serializer = JobApplicationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrReadOnly])
    def search(self, request):
        status = request.query_params.get('status', None)
        job_id = request.query_params.get('job_id', None)
        applicant_id = request.query_params.get('applicant_id', None)

        queryset = self.get_queryset()
        if request.user.role == 'recruiter':
            queryset = queryset.filter(job_id__posted_by=request.user)
        if status:
            queryset = queryset.filter(status=status)
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        if applicant_id:
            queryset = queryset.filter(applicant_id=applicant_id)

        serializer = JobApplicationSerializer(queryset, many=True)
        return Response(serializer.data)

# User ViewSet (unchanged)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ['create', 'register']:
            return UserSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.role == 'applicant':
                ApplicantProfile.objects.create(id=user)
            elif user.role == 'recruiter':
                RecruiterProfile.objects.create(id=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def list_users(self, request):
        queryset = self.get_queryset()
        role = request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)