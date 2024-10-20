from django.views.generic import ListView
from django.shortcuts import render

from publication.models import Publication


# class PublicationListView(ListView):
#     template_name = 'publication.html'
#     model = Publication
#     context_object_name = 'publications'
def publication_list(request, year=None):
    publication = Publication.objects.all()
    if year is None:
        publication = publication[0:3]
    else:
        publication = publication.filter(published_year=year)
    return render(request, 'publication.html', {'publications': publication})