from django.urls import path
from .views import SignupView, LoginView, UserListView
from .views import (
    ApplicantProfileListCreateView, ApplicantProfileRetrieveUpdateView,
    RecruiterProfileListCreateView, RecruiterProfileRetrieveUpdateView
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user-list"),
    # ApplicantProfile endpoints
    path("applicant-profiles/", ApplicantProfileListCreateView.as_view(), name="applicantprofile-list-create"),
    path("applicant-profiles/<int:pk>/", ApplicantProfileRetrieveUpdateView.as_view(), name="applicantprofile-detail"),
    # RecruiterProfile endpoints
    path("recruiter-profiles/", RecruiterProfileListCreateView.as_view(), name="recruiterprofile-list-create"),
    path("recruiter-profiles/<int:pk>/", RecruiterProfileRetrieveUpdateView.as_view(), name="recruiterprofile-detail"),
]
