from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    STATUS = (
        ('current', 'current'),
        ('Alumni', 'Alumni')
    )
    STUDENT_LEVEL = (
        ('Bachelors', 'Bs'),
        ('Master', 'Ms'),
        ('PHD', 'PHD'),
    )
    USER_ROLE = (
        ('student', 'student'),
        ('head', 'head'),
        ('admin', 'admin')
    )

    status = models.CharField(max_length=8, choices=STATUS, blank=True, null=True)
    position = models.CharField(max_length=512, blank=True, null=True)
    student_level = models.CharField(max_length=11, choices=STUDENT_LEVEL, blank=True, null=True)
    professor_verification = models.BooleanField(default=False)
    user_image = models.ImageField(blank=True, upload_to='users', default='img/user/avatar.jpg')
    linkedin_url = models.CharField(max_length=512, blank=True, null=True)
    telegram_url = models.CharField(max_length=512, blank=True, null=True)
    personal_website = models.CharField(max_length=512, blank=True, null=True)
    user_role = models.CharField(max_length=10, choices=USER_ROLE, default=USER_ROLE[0])
    bio = models.CharField(max_length=256, blank=True, null=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
