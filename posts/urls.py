from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post'),
    path('<int:cat_id>', views.PostListView.as_view(), name='post'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='details'),
]
