# accounts/urls.py
from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('user_login/', views.login_view, name='user_login'),  # Use 'user_login' as the name
    path('user_home/', views.user_home, name='user_home'),
    path('user_logout/', views.logout_view, name='user_logout'),


    path('user_home/strength_training/', views.strength_training, name='strength_training'),
        # URL for strength training
    path('user_home/cardio_blast/', views.cardio_blast, name='cardio_blast'),
    path('user_home/flexibility_mobility/',views.flexibility_mobility, name='flexibility_mobility'),
]
