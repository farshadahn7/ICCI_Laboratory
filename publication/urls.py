from django.urls import path

from publication import views
app_name = 'publication'
urlpatterns = [
    path('', views.publication_list, name='publication_list'),
    path('/<str:year>', views.publication_list, name='publication_list'),
]