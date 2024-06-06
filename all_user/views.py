# views.py
from grpc import Status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from .serializers import AllUserSerializer, OutfitSerializer, ImagesSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Outfit, Images

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AllUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=201)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access_token": str(token.access_token),
                "refresh_token": str(token),
                "username": user.username
            })
        return Response({"error": "Invalid credentials"}, status=400)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            serializer = AllUserSerializer(user) 
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class UserOutfitView(generics.ListAPIView):
    serializer_class = OutfitSerializer

    def get_queryset(self):
        # request.user is the authenticated user from the JWT token
        return Outfit.objects.filter(user=self.request.user)


class ImagesCreateView(generics.ListCreateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer




