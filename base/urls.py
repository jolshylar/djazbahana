from django.urls import path
from django.shortcuts import render

from . import views

def balance(request):
    context = {}
    return render(request, 'base/balance.html', context)

urlpatterns = [
    # Authentication
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # Info
    path('', views.home, name='home'),
    path('classroom/<str:pk>/', views.classroom, name='classroom'),
    path('profile/<str:pk>/', views.user_profile, name='user-profile'),
    path('about/', views.about_page, name='about'),
    path('donate/', views.donate_page, name='donate'),
    # Economy
    path('balance/', balance, name='balance'),
    # CRUD endpoints
    path('create-classroom/', views.create_classroom, name='create-classroom'),
    path('update-classroom/<str:pk>/', views.update_classroom, name='update-classroom'),
    path('delete-classroom/<str:pk>/', views.delete_classroom, name='delete-classroom'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('update-user/', views.update_user, name='update-user'),
    # Download
    path('download/<str:filename>/', views.download_file, name='download'),
    # Conspects
    path('create-conspect/<str:pk>/', views.create_conspect, name='create-conspect'),
    # Mobile/Expanded page
    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]
