from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='blog/posts/', default='img/pic/default_post_img.png')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='posts')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:details', args={'pk': self.id})
