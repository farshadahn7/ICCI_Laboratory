from django.db import models


class HomeSliderImage(models.Model):
    cover = models.ImageField(upload_to='home_slider_images')
    cover_link = models.TextField(blank=True)
    cover_title = models.CharField(max_length=128, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cover_title


class GalleryImageCategory(models.Model):
    name = models.CharField(max_length=128, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_images')
    category = models.ForeignKey(GalleryImageCategory, on_delete=models.CASCADE, related_name='cat')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category.name
