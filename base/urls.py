from django.urls import path

from base import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterPageView.as_view(), name='register'),
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutRedirectView.as_view(), name='logout'),
    # Info
    path('', views.HomeView.as_view(), name='home'),
    path('classroom/<str:pk>/', views.classroom, name='classroom'),
    path('u/<str:username>/', views.UserProfileDetailView.as_view(), name='user-profile'),
    # Markdown-Rendering Pages
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('donate/', views.DonatePageView.as_view(), name='donate'),
    # CRUD endpoints
    path('create-classroom/', views.create_classroom, name='create-classroom'),
    path('update-classroom/<str:pk>/', views.update_classroom, name='update-classroom'),
    path('delete-classroom/<str:pk>/', views.delete_classroom, name='delete-classroom'),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),
    path('update-user/', views.update_user, name='update-user'),
    # Conspects
    path('create-conspect/<str:pk>/', views.create_conspect, name='create-conspect'),
    path('delete-conspect/<str:pk>/', views.delete_conspect, name='delete-conspect'),
    path('confirm-payment/<str:pk>/', views.confirm_payment, name='confirm-payment'),
    # Mobile/Expanded page
    path('topics/', views.TopicsPageView.as_view(), name='topics'),
    path('activities/', views.ActivitiesPageView.as_view(), name='activities'),
]
