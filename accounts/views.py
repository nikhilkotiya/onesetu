from django.shortcuts import render
from django.shortcuts import render
from ast import Try
import imp
# from .distance_matrix import  coordinates_preprocesing
import json
from operator import truediv
from select import select
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import APIException
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from .serializers import *
import re
import time
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.utils import timezone
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Define Create User (Register User) API with only post request


class SignupUser(APIView):
    # Handling Post Reuqest
    def post(self, request):
        try:
            serializer = SignupUserSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.create(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    first_name=serializer.validated_data.get('first_name', ''),
                    last_name=serializer.validated_data.get('last_name', ''),
                    mobile=serializer.validated_data.get('mobile', ''),
                )
                user.set_password(serializer.validated_data['password'])
                user.save()
                refresh = RefreshToken.for_user(user)
                if user:
                    json_data = {
                        'status_code': 201,
                        'status': 'Success',
                        'username': str(user),
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': 'User created'
                    }
                    return Response(json_data, status.HTTP_201_CREATED)
                else:
                    json_data = {
                        'status_code': 200,
                        'status': 'Success',
                        'data': 'User not created',
                        'message': 'data not created'
                    }
                    return Response(json_data, status.HTTP_200_OK)
            else:
                print("I am api called-------")
                json_data = {
                    'status_code': 200,
                    'status': 'Failed',
                    'error': serializer.errors,
                    'remark': 'Serializer error'
                }
                return Response(json_data, status.HTTP_200_OK)
        except Exception as err:
            print("Error :", err)
            json_data = {
                'status_code': 500,
                'status': 'Failed',
                'error': f'{err}',
                'remark': 'Landed in exception',
            }
            return Response(json_data, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            # print("iiiiiiiii ",request.id)
            serializer = EditUserProfileSerializer(data=request.data)
            if serializer.is_valid():
                userinfo = User.objects.filter(id=serializer.data.get('id'))
                if userinfo:

                    # print("--------------",userinfo.get("username"))
                    userinfo.update(
                        username=serializer.validated_data.get('username'),
                        email=serializer.validated_data.get('email'),
                        first_name=serializer.validated_data.get(
                            'first_name', ''),
                        last_name=serializer.validated_data.get(
                            'last_name', ''),
                        mobile=serializer.validated_data.get('mobile', '')
                    )
                    json_data = {
                        'status_code': 205,
                        'status': 'Success',
                        'message': 'User updated successfully'
                    }
                    return Response(json_data, status.HTTP_205_RESET_CONTENT)
                else:
                    print("================")
                    json_data = {
                        'status_code': 204,
                        'status': 'Success',
                        'message': 'User not found'
                    }
                    return Response(json_data, status.HTTP_204_NO_CONTENT)
            else:

                json_data = {
                    'status_code': 200,
                    'status': 'Failed',
                    'error': serializer.errors,
                    'remark': 'Serializer error'
                }
                return Response(json_data, status.HTTP_200_OK)
        except Exception as err:
            print("Error :", err)
            json_data = {
                'status_code': 500,
                'status': 'Failed',
                'error': err,
                'remark': 'Landed in exception',
            }
            return Response(json_data, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            # print("iiiiiiiii ",request.id)
            deletestatus, userinfo = User.objects.filter(
                id=request.data.get('id')).delete()
            # print(deletestatus,"--------------",userinfo)
            if deletestatus:
                json_data = {
                    'status_code': 205,
                    'status': 'Success',
                    'message': 'User deleted successfully'
                }
                return Response(json_data, status.HTTP_205_RESET_CONTENT)
            else:
                # print("================")
                json_data = {
                    'status_code': 204,
                    'status': 'Success',
                    'message': 'User not found'
                }
                return Response(json_data, status.HTTP_204_NO_CONTENT)

        except Exception as err:
            print("Error :", err)
            json_data = {
                'status_code': 500,
                'status': 'Failed',
                'error': err,
                'remark': 'Landed in exception',
            }
            return Response(json_data, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginView(APIView):

    def post(self, request, format=None):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = serializer.data.get('username')
                password = serializer.data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    data = User.objects.get(username=user)
                    newdata = {
                        "id": data.id,
                        "username": data.username,
                        "email": data.email,
                        "first_name": data.first_name,
                        "last_name": data.last_name,
                        "mobile": data.mobile,
                        "is_active": data.is_active,
                        "is_superuser": data.is_superuser,
                    }
                    # print("-----------------", newdata)
                    # print("-----------------", type(data))
                    token = get_tokens_for_user(user)
                    json_data = {
                        'status_code': 201,
                        'status': 'Success',
                        'data': newdata,
                        'refresh': str(token.get("refresh")),
                        'access': str(token.get("access")),
                        'message': 'User login success'
                    }
                    return Response(json_data, status.HTTP_201_CREATED)

                else:
                    json_data = {
                        'status_code': 200,
                        'status': 'Failed',
                        'error': "User name or Password is incorrect",
                    }
                    return Response(json_data, status.HTTP_200_OK)
            else:
                print("I am api called-------")
                json_data = {
                    'status_code': 200,
                    'status': 'Failed',
                    'error': serializer.errors,
                    'remark': 'Serializer error'
                }
                return Response(json_data, status.HTTP_200_OK)
        except Exception as err:
            print("Error :", err)
            json_data = {
                'status_code': 500,
                'status': 'Failed',
                'error': f'{err}',
                'remark': 'Landed in exception',
            }
            return Response(json_data, status.HTTP_500_INTERNAL_SERVER_ERROR)

class VelidateAccessToken(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            
            datacheck=User.objects.filter(email=request.user.email)
            #Check Data 
            if datacheck:
                #Getting data of user
                data = User.objects.get(email=request.user.email)
                newdata = {
                    "id": data.id,
                    "username": data.username,
                    "email": data.email,
                    "first_name": data.first_name,
                    "last_name": data.last_name,
                    "mobile": data.mobile,
                    "is_active": data.is_active,
                    "is_superuser": data.is_superuser,
                    "is_zoho_active": data.is_zoho_active,
                }
                
                json_data = {
                    'status_code': 200,
                    'status': 'Success',
                    'data': newdata,
                    'message': 'User token validated'
                }
                return Response(json_data, status.HTTP_200_OK)

            else:
                json_data = {
                    'status_code': 200,
                    'status': 'Failed',
                    'data': '',
                    'error': "User not found",
                }
                return Response(json_data, status.HTTP_200_OK)
        
        except Exception as err:
            print("Error :", err)
            json_data = {
                'status_code': 500,
                'status': 'Failed',
                'error': err,
                'remark': 'Landed in exception',
            }
            return Response(json_data, status.HTTP_500_INTERNAL_SERVER_ERROR)


