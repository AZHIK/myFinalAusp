from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,CustomUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
    )
    username = forms.CharField(
       label='',
       help_text="" ,
       widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )

    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        help_text="Password must be at least 8 characters long and not too common.",
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        help_text="",
    )

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(
       label='Phone',
       help_text="Start with your country code, e.g., +91 XXXXXXXXX",
       widget=forms.TextInput(attrs={'placeholder': '+91 XXXXXXXXX'}),
    )

    program = forms.CharField(
       label='Program',
       help_text="Write in long form, e.g., BSc Software Engineering",
       widget=forms.TextInput(attrs={'placeholder': 'BSc Software Engineering'}),
    )

    class Meta:
        model = UserProfile
        fields = ("firstname", "last_name", "category_of_membership", "nationality", "current_residential_country", "phone", "name_of_institute", "program", "duration_of_studies", "year", "profile_image")

    profile_image = forms.ImageField(required=False)
    year = forms.IntegerField(
       label='Year of Completion'
    )
