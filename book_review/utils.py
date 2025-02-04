import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from Users.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  exceptions, authentication


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        auth_data = authentication.get_authorization_header(request).decode('utf-8')

        if not auth_data or not auth_data.startswith('Bearer '):
            # raise exceptions.AuthenticationFailed({"error": "Authentication credentials were not provided or are invalid."},code=status.HTTP_401_UNAUTHORIZED,)
            return None
        token = auth_data.split(' ')[1]
        if not token:
            return Response({"error": "Token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            raise AuthenticationFailed({"error":"Token has expired"}, code=status.HTTP_401_UNAUTHORIZED)
        except InvalidTokenError:
            raise AuthenticationFailed( {"error": "Invalid token"}, code=status.HTTP_401_UNAUTHORIZED)

    
        email = payload.get("email") 
        if not email:
            raise exceptions.AuthenticationFailed(
                {"error": "Email is missing from the token payload"},
                code=status.HTTP_401_UNAUTHORIZED,
            )

        user= User.objects.filter(email=email).first()
        if not user:
            raise exceptions.AuthenticationFailed(
                {"error": "User not found"}, code=status.HTTP_401_UNAUTHORIZED
            )
        return (user, None)
        
        
           

      

def auth_by_token(request):
    try:
        jwt_auth= JWTAuthentication()
        auth= jwt_auth.authenticate(request)
        if auth:
            return auth[0]
        else:
            return Response(
                {"error": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except exceptions.AuthenticationFailed:
        return exceptions.AuthenticationFailed