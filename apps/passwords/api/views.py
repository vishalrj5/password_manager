import logging
from apps.passwords.api.schemas import UserPasswordsSchema
from apps.passwords.api.serializers import PasswordRegisterSerializer
from apps.passwords.models import UserPasswords
from apps.users.models import Users
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import generics,status
from password_management.helpers.pagination import RestPagination
from rest_framework import filters
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from password_management.response import ResponseInfo
from apps.authentication.api.serializers import RefreshTokenSerializer, UserRegisterSerializer, LoginSerializer, LogoutSerializer, OTPSerializer, UserRegisterUpdateSerializer
from apps.authentication.api.schemas import FinalRegistrationPostSchema, FinalRegistrationSchema, LoginPostSchema, LoginSchema, RegisterPostSchema, RegisterSchema, UsersSchema, VerifyOTPPostSchema


logger = logging.getLogger(__name__)


class CreatePasswordAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreatePasswordAPIView, self).__init__(**kwargs)

    serializer_class = PasswordRegisterSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(tags=["Create Password"])
    def post(self, request):
        try:
            messages = "Password Created Successfully"
            serializer = self.serializer_class(data=request.data, context = {'request' : request})

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            password_instance = serializer.validated_data.get('user_passwod', None)
            if password_instance:
                if UserPasswords.objects.filter(Q(edit_users=request.user.id) & Q(id=password_instance.id)):
                    messages = "Password Updated Successfully"

                    serializer = self.serializer_class(password_instance, data=request.data, context = {'request' : request})
                    
                    if not serializer.is_valid():
                        self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                        self.response_format["status"] = False
                        self.response_format["errors"] = serializer.errors
                        return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                else:
                    self.response_format['status_code'] = status.HTTP_401_UNAUTHORIZED
                    self.response_format["status"] = False
                    self.response_format["errors"] = "Not Authorized to perform this action."
                    return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)
                
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = messages
            self.response_format["status"] = True
            self.response_format["data"] = serializer.data
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePasswordAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdatePasswordAPIView, self).__init__(**kwargs)

    serializer_class = PasswordRegisterSerializer

    @swagger_auto_schema(tags=["Update Password"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context = {'request' : request})

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            password_instance = serializer.validated_data.get('id', None)
            print("pppppppp ", password_instance)
            serializer = self.serializer_class(password_instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = "Password Updated Successfully"
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetUserPasswordsApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetUserPasswordsApiView, self).__init__(**kwargs)
        
    queryset = UserPasswords.objects.all().order_by('-id')
    serializer_class = UserPasswordsSchema
    permission_classes = (IsAuthenticated,)
    
    pagination_class = RestPagination
    
    @swagger_auto_schema(pagination_class=RestPagination, tags=["Users"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_instance = self.request.user
        
        if user_instance:
            print(">>>>>>>> ", user_instance.id)
            queryset = queryset.filter(Q(view_users=user_instance.id) | Q(user_id=user_instance.id)).distinct()
            print("queyset ", queryset)
            page = self.paginate_queryset(queryset)
        
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return None
