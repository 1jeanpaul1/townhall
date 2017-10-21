from django.conf.urls import url

from . import views
from views import HomeView, UserRegistrationView, LogoutView
from django.contrib.auth.views import login, login_required

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^profile/$', views.ProfileView, name='profile'),
    url(r'^login/$', login, {'template_name': 'townhall/login.html'}),
    # url(r'^login/$', views.login, name='login'),
# auth_view
#     url(r'^auth_view/$', views.auth_view, name='auth_view'),
    url(r'^register/$', UserRegistrationView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
]