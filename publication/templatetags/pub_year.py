from django.template import Library
from publication.models import Publication

register = Library()


@register.inclusion_tag('get_pub_year.html')
def pub_year():
    data = Publication.objects.values('published_year').distinct()
    years = []
    for y in data:
        years.append(y['published_year'])
    return {'years': years}
