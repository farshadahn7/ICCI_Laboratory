from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import CustomUserChangeForm
from accounts.models import CustomUser
from accounts.forms import CustomUserChangeForm, CustomUserForm, UserProfileForm
from posts.forms import PostForm
from posts.models import Post
from category.models import Category
from category.forms import CategoryForm
from publication.models import Publication
from publication.forms import PublicationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from pages.models import GalleryImage, GalleryImageCategory
from pages.forms import ImageGalleryForm


class AdminPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_role in ['admin', 'head']


class HeadPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_role.lower() == "head"


class PermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_role.lower() in ["head", 'admin', 'student']


class PanelView(LoginRequiredMixin, AdminPermissionMixin, generic.ListView):
    model = CustomUser
    template_name = 'panel/index_panel.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        user_data = CustomUser.objects.all()
        context_object_name['phdCount'] = user_data.filter(student_level="PHD", status='current',
                                                           professor_verification=True).count()
        context_object_name['masterCount'] = user_data.filter(student_level="Master", status='current',
                                                              professor_verification=True).count()
        context_object_name['allStudent'] = user_data.filter(student_level__in=['Bachelors', 'Master', 'PHD'],
                                                             status__in=['current', 'Alumni'],
                                                             professor_verification=True).count()
        context_object_name['alumniStudent'] = user_data.filter(professor_verification=True, status='Alumni').count()
        context_object_name['newStudents'] = user_data.filter(professor_verification=False)
        context_object_name['admins'] = user_data.filter(professor_verification=True,
                                                         status__in=['current', 'Alumni'],
                                                         student_level__in=['Bachelors', 'Master', 'PHD'],
                                                         user_role='admin')
        return context_object_name


class UserListView(AdminPermissionMixin, generic.ListView):

    def get(self, request, *args, **kwargs):
        level = kwargs.get('level')
        users = CustomUser.objects.filter(professor_verification=True, student_level__in=['Bachelors', 'Master', 'PHD'],
                                          status__in=['current', 'Alumni'])
        if level is not None:
            if level != 'Alumni':
                users = users.filter(student_level=level, status='current')
            else:
                users = users.filter(status=level)
        return render(request, 'panel/user_list.html', {'users': users})


class UserUpdateView(AdminPermissionMixin, generic.UpdateView):
    model = CustomUser
    fields = ['status', 'student_level', 'user_role','professor_verification']
    template_name = 'panel/edite_user.html'
    context_object_name = 'student_user'
    success_url = reverse_lazy('panel:panel_home')


@login_required
@user_passes_test(lambda u: u.user_role == 'head', login_url='accounts:login_view')
def delete_user(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.delete()
    return redirect('panel:user_list')


@login_required
@user_passes_test(lambda u: u.user_role == 'admin' or 'head', login_url='accounts:login_view')
def verify_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.professor_verification = True
    user.save()
    return redirect('panel:edite_user', user.id)


class AdminListView(HeadPermissionMixin, generic.ListView):
    # permission_required = 'publication.view_panel'
    model = CustomUser
    template_name = 'panel/admin_list.html'
    context_object_name = 'admins'

    def get_queryset(self):
        admins = CustomUser.objects.filter(professor_verification=True, status__in=['current', 'Alumni'],
                                           student_level__in=['Bachelors', 'Master', 'PHD'],
                                           user_role='admin')
        return admins


@login_required
@user_passes_test(lambda u: u.user_role == 'head', login_url='accounts:login_view')
def make_admin(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.user_role = 'admin'
    user.save()
    return redirect('panel:admin_list')


@login_required
@user_passes_test(lambda u: u.user_role == 'head', login_url='accounts:login_view')
def un_role(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.user_role = 'student'
    user.save()
    return redirect('panel:admin_list')


class PostListView(AdminPermissionMixin, generic.ListView):
    # permission_required = 'publication.view_panel'
    model = Post
    template_name = 'panel/posts.html'
    context_object_name = 'posts'


class NewPostView(AdminPermissionMixin, generic.CreateView):
    model = Post
    # form_class = PostForm
    fields = ['title', 'content', 'image', 'category', 'status']
    template_name = 'panel/new_post.html'
    success_url = reverse_lazy('panel:post_lists')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# @login_required
# @user_passes_test(lambda u: u.user_role in ['head', 'admin'], login_url='accounts:login_view')
# def update_post(request, pk):
#     post = Post.objects.filter(pk=pk).first()
#     category = Category.objects.all()
#     form = PostForm(request.POST or None, instance=post)
#     if request.method == 'POST':
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('panel:post_lists')
#     else:
#         context = {'form': form, 'category': category}
#         return render(request, template_name='panel/new_post.html', context=context)

class UpdatePostView(AdminPermissionMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'status']
    # form_class = PostForm
    template_name = 'panel/new_post.html'

    def get_success_url(self):
        return reverse_lazy('panel:post_lists')


@login_required
@user_passes_test(lambda u: u.user_role in ['head', 'admin'], login_url='accounts:login_view')
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('panel:post_lists')


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'panel/profile.html'


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form = UserProfileForm
    fields = ['username', 'first_name', 'last_name', 'email', 'user_image', 'linkedin_url', 'telegram_url', 'bio',
              'position']
    template_name = 'panel/profile_update.html'

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse_lazy('panel:profile', kwargs={'pk': pk})
    # def get(self, request, *args, **kwargs):
    #     user_id = kwargs.get('pk')
    #     user = CustomUser.objects.get(pk=user_id)
    #     form = UserProfileForm(instance=user)
    #     context = {'form': form}
    #     return render(request, template_name='panel/profile_update.html', context=context)
    #
    # def post(self, request, *args, **kwargs):
    #     user_id = kwargs.get('pk')
    #     user = CustomUser.objects.get(pk=user_id)
    #     form = UserProfileForm(request.POST, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('panel:profile', user.id)


class CategoryCreateView(AdminPermissionMixin, generic.CreateView):
    model = Category
    # permission_required = 'publication.view_panel'
    form_class = CategoryForm
    template_name = 'panel/new_category.html'
    success_url = reverse_lazy('panel:category_list')


class CategoryListView(AdminPermissionMixin, generic.ListView):
    model = Category
    # permission_required = 'publication.view_panel'
    template_name = 'panel/categories.html'
    context_object_name = 'cats'


@login_required
@user_passes_test(lambda u: u.user_role in ['head', 'admin'], login_url='accounts:login_view')
def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    return redirect('panel:category_list')


class CategoryUpdateView(AdminPermissionMixin, generic.UpdateView):
    model = Category
    form_class = CategoryForm
    # permission_required = 'publication.view_panel'
    template_name = 'panel/new_category.html'
    context_object_name = 'cat'
    success_url = reverse_lazy('panel:category_list')


class PublicationListView(AdminPermissionMixin, generic.ListView):
    # permission_required = 'publication.view_panel'
    model = Publication
    template_name = 'panel/publications.html'
    context_object_name = 'pubs'


@login_required
@user_passes_test(lambda u: u.user_role in ['head', 'admin'], login_url='accounts:login_view')
def delete_publication(request, pub_id):
    pub = Publication.objects.get(pk=pub_id)
    pub.delete()
    return redirect('panel:publication_list')


class PublicationCreateView(AdminPermissionMixin, generic.CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'panel/new_publication.html'
    success_url = reverse_lazy('panel:publication_list')


class PublicationUpdateView(AdminPermissionMixin, generic.UpdateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'panel/new_publication.html'
    context_object_name = 'pub'
    success_url = reverse_lazy('panel:publication_list')


class GalleryListView(LoginRequiredMixin, generic.ListView):
    model = GalleryImage
    template_name = 'panel/galleries.html'
    context_object_name = 'galleries'


class GalleryCreateView(LoginRequiredMixin, generic.CreateView):
    model = GalleryImage
    form_class = ImageGalleryForm
    template_name = 'panel/new_gallery.html'
    context_object_name = 'gallery'
    success_url = reverse_lazy('panel:gallery')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        context_object_name['cats'] = GalleryImageCategory.objects.all()
        return context_object_name


class GalleryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = GalleryImage
    form_class = ImageGalleryForm
    template_name = 'panel/new_gallery.html'
    context_object_name = 'gallery'
    success_url = reverse_lazy('panel:gallery')

    def get_context_data(self, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        context_object_name['cats'] = GalleryImageCategory.objects.all()
        return context_object_name


def delete_gallery(request, pk):
    gallery = get_object_or_404(GalleryImage, pk=pk)
    gallery.delete()
    return redirect('panel:gallery')
