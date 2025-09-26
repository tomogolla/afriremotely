from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import JobPostingViewSet, CategoryViewSet, LocationViewSet

# Swagger schema view 
schema_view = get_schema_view(
    openapi.Info(
        title="Afriremotely API",
        default_version='v1',
        description="API for Afriremotely job board platform",
        contact=openapi.Contact(email="thomasogolla637@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router for viewsets
router = DefaultRouter()
router.register(r'jobs', JobPostingViewSet, basename='job-posting')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'locations', LocationViewSet, basename='location')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/openapi/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]