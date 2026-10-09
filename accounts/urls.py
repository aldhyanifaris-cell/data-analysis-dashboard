"""
Accounts API URLs.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('profile/', views.ProfileView.as_view(), name='auth_profile'),
    path('preferences/', views.UpdatePreferencesView.as_view(), name='auth_preferences'),
]
