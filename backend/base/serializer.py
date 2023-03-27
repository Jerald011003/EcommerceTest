from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import Product
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
# from .models import UserProfile


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d")
    name=serializers.SerializerMethodField(read_only=True)
    _id=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin','password', 'date_joined','first_name' ]
        # fields='__all__'
    def get_name(self,obj):
        name=obj.first_name
        if name=="":
            name=obj.email
        return name
    
    def get__id(self,obj):
        return obj.id

    def get_isAdmin(self,obj):
        return obj.is_staff

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'

class UserSerializerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=User
        fields=['id','_id','username','email','name','isAdmin','token']
    
    def get_token(self,obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)