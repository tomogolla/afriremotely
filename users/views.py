from rest_framework import generics, permissions
from .serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import User
from .models import ApplicantProfile, RecruiterProfile
from .serializers import ApplicantProfileSerializer, RecruiterProfileSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ApplicantProfile API Views
class ApplicantProfileListCreateView(generics.ListCreateAPIView):
    queryset = ApplicantProfile.objects.all()
    serializer_class = ApplicantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApplicantProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ApplicantProfile.objects.all()
    serializer_class = ApplicantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

# RecruiterProfile API Views
class RecruiterProfileListCreateView(generics.ListCreateAPIView):
    queryset = RecruiterProfile.objects.all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class RecruiterProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = RecruiterProfile.objects.all()
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]