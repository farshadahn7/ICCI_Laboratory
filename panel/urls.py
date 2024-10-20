from django.urls import path
from panel import views

app_name = 'panel'
urlpatterns = [
    path('', views.PanelView.as_view(), name='panel_home'),
    path('users', views.UserListView.as_view(), name='user_list'),
    path('users/<str:level>', views.UserListView.as_view(), name='user_list'),
    path('admin', views.AdminListView.as_view(), name='admin_list'),
    path('posts', views.PostListView.as_view(), name='post_lists'),
    path('new_post', views.NewPostView.as_view(), name='new_post'),
    path('update_post/<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('edite_user/<int:pk>', views.UserUpdateView.as_view(), name='edite_user'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('verify_user/<int:user_id>', views.verify_user, name='verify_user'),
    path('make_admin/<int:user_id>', views.make_admin, name='make_admin'),
    path('un_role/<int:user_id>', views.un_role, name='un_role'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile_update/<int:pk>', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('new_category/', views.CategoryCreateView.as_view(), name='new_category'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('delete_category/<int:category_id>', views.delete_category, name='category_delete'),
    path('update_category/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
    path('publication/', views.PublicationListView.as_view(), name='publication_list'),
    path('create_publication/', views.PublicationCreateView.as_view(), name='new_publication'),
    path('delete_publication/<int:pub_id>', views.delete_publication, name='publication_delete'),
    path('update_publication/<int:pk>', views.PublicationUpdateView.as_view(), name='publication_update'),
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('add_image/', views.GalleryCreateView.as_view(), name='create_gallery'),
    path('update_image/<int:pk>', views.GalleryUpdateView.as_view(), name='edite_gallery'),
    path('delete_image/<int:pk>', views.delete_gallery, name='delete_gallery'),
]
