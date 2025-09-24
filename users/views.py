from rest_framework import generics
from .serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status

class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
