from django.conf.urls import url

from . import views
from views import HomeView
from django.contrib.auth.views import login, login_required

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^home/$', HomeView.as_view(), name='home'),
    # url(r'^login/$', login, {'template_name': 'townhall/login.html'})
    url(r'^login/$', views.login, name='login'),
]