from django.contrib.auth.models import User
from base.models import Product
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .serializer import ProductSerializer,UserSerializer,UserSerializerWithToken,OrderSerializer, UserUpdateSerializer
from .products import products
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import mimetypes
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
# from .models import UserProfile
# from .serializer import UserProfileSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',

        '/api/products/upload/',

        '/api/products/<id>/reviews/',

        '/api/products/top/',
        '/api/products/<id>/',

        '/api/products/delete/<id>/',
        '/api/products/<update>/<id>',
    ]
    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    product=Product.objects.get(_id=pk)
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)


@api_view(['GET'])
def download_file(request, pk):
    product = Product.objects.get(_id=pk)
    file_path = product.download.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read())
        content_type, encoding = mimetypes.guess_type(file_path)
        response['Content-Type'] = content_type
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(file_path))
        return response



    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,attrs):
        data=super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
    

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    
@api_view(['POST'])
def registerUser(request):
    data=request.data
    print(data)
    try:

        user=User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer=UserSerializerWithToken(user,many=False)
        return Response(serializer.data)
    except:
        message={'details':'USER WITH THIS EMAIL ALREADY EXIST'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)


# #Youtube User Update

class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            user_profile = User.objects.get(id=user.id)
            user_profile_serialized = UserSerializer(user_profile)

            return Response({ 'profile': user_profile_serialized.data, 'username': str(username) })
        except User.DoesNotExist:
            return Response({ 'error': 'User does not exist' }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class UpdateUserProfileView(APIView):
#     def put(self, request, format=None):
#         try:
#             user = self.request.user
#             username = user.username

#             data = self.request.data
#             username_data = data.get('username')
#             email_data = data.get('email')

#             user_obj = User.objects.filter(id=user.id).first()
#             if username_data:
#                 user_obj.username = username_data
#             if email_data:
#                 user_obj.email = email_data
#             user_obj.save()

#             user_profile = User.objects.filter(user=user_obj).first()
#             if user_profile:
#                 if username_data:
#                     user_profile.username = username_data
#                 if email_data:
#                     user_profile.email = email_data
#                 user_profile.save()

#             user_profile_serialized = UserSerializerWithToken(user_obj)

#             return Response({ 'profile': user_profile_serialized.data, 'username': str(username) })
#         except:
#             return Response({ 'error': 'Something went wrong when updating profile' })


class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        try:
            user = self.request.user

            data = self.request.data
            user_update_serializer = UserUpdateSerializer(user, data=data, partial=True)
            user_update_serializer.is_valid(raise_exception=True)
            user_update_serializer.save()

            user_serializer = UserSerializer(user)

            return Response(user_serializer.data)
        except:
            return Response({ 'error': 'Something went wrong when updating profile' }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)