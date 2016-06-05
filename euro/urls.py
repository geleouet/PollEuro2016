from django.conf.urls import url

from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'euro'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^save$', views.save, name='save'),
    url(r'^nexts$', views.next_matchs, name='nexts'),
    url(r'^check_login$', views.check_login, name='check_login'),
    url(r'^register$', views.register, name='register'),
    url(r'^change_team$', views.change_team, name='change_team'),
    url(r'^classement$', views.classement, name='classement'),
    url(r'^member_id/(?P<mid>[0-9]+)/$', views.view_member, name='member_id'),
    url(r'^teams$', views.classement_teams, name='teams'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^landing$', views.landinPage, name='landingpage'),

    url(r'^team_id/(?P<mid>[0-9]+)/$', views.team, name='team'),
    url(r'^change_desc/(?P<mid>[0-9]+)/$', views.change_desc, name='change_desc'),


    url(r'^logout$', views.logout_view, name='logout'),
]