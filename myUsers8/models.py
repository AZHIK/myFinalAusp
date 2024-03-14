import os
import secrets  # Secure random number generation
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from django.conf import settings
import pycountry

membership_category = (
    ("Honorary", "Honorary"),
    ("Associates", "Associates"),
    ("Ordinary", "Ordinary"),
    ("Special", "Special"),
)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    Bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    category_of_membership = models.CharField(
        choices=membership_category, max_length=30, default="Ordinary"
    )
    firstname = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=13)
    nationality = models.CharField(
        max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,
    )
    current_residential_country = models.CharField(
        max_length=100,
        choices=[(country.name, country.name) for country in pycountry.countries],
        blank=True,
        null=True,
    )
    name_of_institute = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    duration_of_studies = models.IntegerField(default=0)
    year = models.IntegerField(default=2020)
    identification_number = models.CharField(max_length=30, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)  # Image field

    def save(self, *args, **kwargs):
        if not self.identification_number:
            token = secrets.token_hex(3).upper()  # Generating token and converting to uppercase
            self.identification_number = f"{os.getenv('ID_PREFIX', 'AUSP')}/{datetime.now().year}/{token}"  # Secure generation
        super().save(*args, **kwargs)

    def get_profile_image_url(self):
        """
        Returns the URL of the user's profile image or a default image if none exists.
        """
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return os.path.join(settings.MEDIA_URL, 'default_profile_image.jpg')  # Customize default image path

    class Meta:
        verbose_name_plural = "User profiles"
