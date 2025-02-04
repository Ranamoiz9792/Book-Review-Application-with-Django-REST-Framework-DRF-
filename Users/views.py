from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .serializer import SignupSerializer, LoginSerializer
from .utils import generate_otp, send_email, generate_email_body, generate_jwt_token
import jwt
import datetime
from django.contrib.auth import authenticate
from django.conf import settings

class SignupViewSet(viewsets.ViewSet):
    def create(self, request):
        """Handles signup request, stores data in cache, and sends OTP."""
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if User.objects.filter(email=email).exists():
            return Response({"details": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"details": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate OTP and store user data in cache (valid for 10 mins)
        otp = str(generate_otp())
        cache.set(email, {'username': username, 'email': email, 'password': password, 'otp': otp}, timeout=600)

        # Send OTP via email
        email_body = generate_email_body(otp)
        email_sent = send_email(email, "Login Verification Code", email_body)

        if not email_sent:
            return Response({"details": "Failed to send OTP, please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"details": "OTP sent to email"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """Handles OTP verification and saves user if OTP is correct."""
        email = request.data.get('email')
        otp = request.data.get('otp')

        # Get cached user data
        cached_data = cache.get(email)
        if not cached_data:
            return Response({"details": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if cached_data['otp'] != otp:
            return Response({"details": "Incorrect OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Save user to database
        hashed_password = make_password(cached_data['password'])
        user = User.objects.create(
            username=cached_data['username'],
            email=cached_data['email'],
            password=hashed_password
        )

        # Remove data from cache after successful signup
        cache.delete(email)

        return Response({"details": "User created successfully", "username": user.username}, status=status.HTTP_201_CREATED)


class LoginViewSet(viewsets.ViewSet):
    
    def create(self, request):
        """Handles login request."""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate user
        user =User.objects.filter(email=email).first()
        if user is None:
            return Response({"details": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_password(password, user.password):
            token = generate_jwt_token(user.email)
            return Response({"details": "Login successful", "token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"details": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)



        

    