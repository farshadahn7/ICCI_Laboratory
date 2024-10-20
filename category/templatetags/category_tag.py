from django import template
from category.models import Category
from django.db.models import Count
from django.db.models import Q

register = template.Library()


@register.inclusion_tag('category_list.html')
def category_list():
    categories = Category.objects.annotate(number_of_cat=Count("posts", filter=Q(posts__status=True))).all()
    category_lists = Category.objects.all()
    cat_list = []
    for category in categories:
        cat_list.append(
            {'name': category.name, 'number_of_cat': category.number_of_cat, 'id':category.id}
        )
    return {'category_lists': cat_list}
