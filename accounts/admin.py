from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('status', 'position', 'student_level', 'professor_verification',  'user_image', 'linkedin_url', 'telegram_url', 'user_role','personal_website', 'bio')
        }),
    )
    add_fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('status', 'position', 'student_level', 'professor_verification',  'user_image', 'linkedin_url', 'telegram_url', 'personal_website','user_role', 'bio')
        }),
    )
