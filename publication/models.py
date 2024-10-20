from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=384)
    file = models.FileField(upload_to='publications/', default=None, null=True, blank=True)
    author = models.CharField(max_length=384)
    published_at = models.CharField(max_length=384)
    published_at_detail = models.CharField(max_length=512, default='test')
    published_year = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
