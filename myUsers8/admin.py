import secrets
import os
from io import BytesIO
from zipfile import ZipFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.contrib import admin
from django.utils.html import mark_safe
from django.conf import settings
from .models import UserProfile
from import_export.admin import ImportExportModelAdmin
from .models_resource import UserProfileResource
import requests  # Import the requests library

class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ["firstname", "last_name", "identification_number", "category_of_membership", "nationality", "current_residential_country", "name_of_institute", "program", "duration_of_studies", "year", "get_profile_image"]
    actions = ['download_profile_images']

    def download_profile_images(self, request, queryset):
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for obj in queryset:
                if obj.profile_image:
                    image_name = f"{obj.identification_number}.jpg"  # Rename the image with the identification number
                    image_path = os.path.join(settings.MEDIA_ROOT, obj.profile_image.name)
                    if default_storage.exists(image_path):
                        zip_file.write(image_path, arcname=image_name)  # Use the renamed image name in the ZIP file

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="profile_images.zip"'
        return response

    download_profile_images.short_description = "Download profile images"

    def get_profile_image(self, obj):
        """
        Returns the user's profile image as an HTML image tag.
        """
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return mark_safe(f'<img src="{obj.profile_image.url}" width="100" height="50" />')
        else:
            return "No image uploaded"


    get_profile_image.short_description = 'Profile Image'
    resources_class = UserProfileResource

admin.site.register(UserProfile, UserProfileAdmin)













