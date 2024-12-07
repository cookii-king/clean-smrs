from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AccountSerializer
from .models import Account
import datetime
import jwt
from django.shortcuts import render

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header:
            try:
                token_type, token = auth_header.split()
                if token_type.lower() != 'bearer':
                    raise AuthenticationFailed('Invalid token type')
            except ValueError:
                raise AuthenticationFailed('Invalid token header')
        else:
            token = request.COOKIES.get('jwt')

        if not token:
            return None
        try:
            payload = jwt.decode(token, 'secret-key', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        account = Account.objects.filter(id=payload['id']).first()
        if account is None:
            raise AuthenticationFailed('User not found')

        return (account, None)
    
class AccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        return render(request, 'register.html')
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        account = Account.objects.filter(email=email).first()

        if account is None:
            raise AuthenticationFailed('Account not found!')

        if not account.check_password(password):
            raise AuthenticationFailed('Incorrect email or password!')

        # Convert UUID to string
        payload = {
            'id': str(account.id),  # Convert UUID to string
            'username': str(account.username),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret-key', algorithm='HS256')

        response = Response({'message': 'successful!'})
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    def get(self, request):
        return render(request, 'login.html')
    
class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        print(f"jwt token: {token}")
        response = Response()
        response.delete_cookie('jwt')
        response.data = {"message": "success"}
        return response
    
    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(f"jwt token: {token}")
        response = Response()
        response.delete_cookie('jwt')
        response.data = {"message": "success"}
        return response
