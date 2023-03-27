from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
   
)
from .views import GetUserProfileView, UpdateUserProfileView, getUsers


urlpatterns = [
    path('',views.getRoutes,name="getRoutes"),
    path('users/register/',views.registerUser,name='register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),


    path('products/<str:pk>/download', views.download_file, name='download_file'),
    path('products/',views.getProducts,name="getProducts"),
    path('products/<str:pk>',views.getProduct,name="getProduct"),

    # path('update', UpdateUserProfileView.as_view()),

    path('login/', views. MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('register', views.registerUser, name='register'), 
    path('update/', UpdateUserProfileView.as_view(), name='update-user-profile'),
    path('user', GetUserProfileView.as_view()),
    path('users', views.getUsers, name="users"),
    # path('update', views.UpdateUserProfileView, name='updateuser'),
     # path('profile/update', views.updateUserProfile, name="user-profile-update"), 
]
