from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.user.is_authenticated:
        return redirect("edit_profile")
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(user=user)
            # Automatically log in the user
            login(request, user)
            return redirect("profile_view")  # Redirect to profile view page
    else:
        form = UserRegistrationForm()
        

    return render(request, "register.html", {"form":form})

def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect("home")
        

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    # profile = request.user.userprofile
    profile = getattr(request.user, 'userprofile', None)
    if profile:
        if request.method == "POST":
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
        else:
            form = UserProfileForm(instance=profile)
        return render(request, "edit_profile.html", {"form": form})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")
    


@login_required
def home(request):
    return render(request,'home.html')


@login_required
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    profile = getattr(request.user, 'userprofile', None)
    if profile:
        return render(request, "profile_view.html", {"profile": profile})
    else:
        error_message = "You don't have any profile you may logout or contact you system admin."
        messages.warning(request, error_message)
        return redirect("home")
    
