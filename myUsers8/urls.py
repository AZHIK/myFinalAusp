from django.urls import path
from . import views
from .admin import UserProfileAdmin



urlpatterns = [
    path("", views.login_view, name="login"),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('admin/logout/', views.logout_view, name='custom_logout'),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile_view"),
    path('admin/download-profile-images/', UserProfileAdmin.download_profile_images, name='download_profile_images'),
]
