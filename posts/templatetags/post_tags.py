from django import template
from posts.models import Post

register = template.Library()


@register.inclusion_tag('latest_posts.html')
def latest_posts():
    posts = Post.objects.filter(status=True).order_by('-created_at')[:2]
    return {'latest_posts': posts}
