from django.db import models


class Contact(models.Model):
    username = models.CharField(max_length=192)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
