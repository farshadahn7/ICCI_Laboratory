from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from django.shortcuts import render

from posts.forms import PostForm
from posts.models import Post
from category.models import Category


class PostListView(ListView):
    # model = Post
    template_name = 'blog.html'
    # context_object_name = 'posts'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        cat_id = self.kwargs.get('cat_id')
        posts = Post.objects.filter(status=True).order_by('-created_at')
        category = Category.objects.all()
        if cat_id is not None:
            posts = posts.filter(category__id=cat_id)
            cat_name_of_page = posts.first().category.name
            context = {'posts': posts, 'category': category, 'cat_name_of_page': cat_name_of_page}
            return render(request, self.template_name, context)
        else:
            cat_name_of_page = 'All Categories'
            context = {'posts': posts, 'category': category, 'cat_name_of_page': cat_name_of_page}
            return render(request, self.template_name, context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post-details.html'
    context_object_name = 'post'
