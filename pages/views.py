from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

from pages.models import HomeSliderImage
from posts.models import Post

from pages.models import GalleryImageCategory, GalleryImage


class Home(generic.ListView):
    model = HomeSliderImage
    template_name = 'index.html'
    context_object_name = 'slider_contents'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        context_object_name['posts'] = Post.objects.filter(status=True).order_by('-created_at')
        return context_object_name


class GalleryView(generic.ListView):
    template_name = 'gallery.html'
    model = GalleryImage
    context_object_name = 'images'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        context_object_name['cats'] = GalleryImageCategory.objects.all()
        return context_object_name
