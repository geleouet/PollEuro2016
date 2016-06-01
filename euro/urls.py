from django.conf.urls import url

from . import views

app_name = 'euro'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^save$', views.save, name='save'),
    url(r'^nexts$', views.next_matchs, name='nexts'),
    url(r'^check_login$', views.check_login, name='check_login'),
    url(r'^register$', views.register, name='register'),
    url(r'^classement$', views.classement, name='classement'),
    url(r'^teams$', views.manageteam, name='teams'),
    url(r'^succes$', views.addUserToTeam, name='succes'),

    url(r'^logout$', views.logout_view, name='logout'),
        

]