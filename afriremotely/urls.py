


from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="AfriRemotely API",
      default_version="v1",
      description="API documentation for AfriRemotely Job Board",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="thomasogolla637@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/jobs/", include("jobs.urls")),
    # path("api/applications/", include("applications.urls")),

    # swagger + redoc
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/openapi/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]









# schema_view = get_schema_view(
#     openapi.Info(
#         title="Job Board API",
#         default_version='v1',
#         description="API documentation for Job Board Backend",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('jobs.urls')),
#     path('api/', include('api.urls')),
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
#     path("api/users/", include("users.urls")),
    
# ]
