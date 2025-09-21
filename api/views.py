from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from jobs.models import JobPosting, Category, Location
from jobs.serializers import JobPostingSerializer, JobPostingListSerializer, CategorySerializer, LocationSerializer
from users.models import User

# Custom Permission for Role-Based Access
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

class IsAuthenticatedApplicant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'applicant'

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
            queryset = queryset.filter(category_id__name__iexact=category)
        if location:
            queryset = queryset.filter(location_id__city__iexact=location)
        if work_mode:
            queryset = queryset.filter(work_mode=work_mode)

        serializer = JobPostingListSerializer(queryset, many=True)
        return Response(serializer.data)

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

# Location ViewSet
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAdminOrReadOnly]