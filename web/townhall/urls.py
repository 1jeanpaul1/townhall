from django.conf.urls import url

from . import views
from views import AllPostsView, UserRegistrationView, LogoutView, ProfileView, LoginView, UserFormPostView,\
    FeedView, SavedPostsView
from django.contrib.auth.views import login, login_required

def check_login(view_function):
    return login_required(view_function.as_view(), redirect_field_name="", login_url='/login/')

login_url = '/townhall/login/'
urlpatterns = [
    url(r'^home/$', login_required(FeedView.as_view()), name='home'),
    url(r'^home/all_posts/$', login_required(AllPostsView.as_view()), name='all_posts'),
    url(r'^home/saved_posts/$', login_required(SavedPostsView.as_view()), name='saved_posts'),
    # url(r'^login/$', login, {'template_name': 'townhall/login.html'}, name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', UserRegistrationView.as_view(), name='register'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),
    url(r'^user/([0-9]+)$', login_required(ProfileView), name = 'profile'),
    url(r'^newpost/$', login_required(UserFormPostView.as_view()), name='newpost'),
    url(r'^post/([0-9]+)$', views.getPost, name='get_post_data'),
    # url(r'^post/([0-9]+)$', login_required(views.getPost()), name = 'post'),
    # url(r'^feed/$', FeedView.as_view(), name='feed'),
]