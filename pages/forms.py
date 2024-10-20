from django import forms

from pages.models import GalleryImage


class ImageGalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image', 'category']
