from django.conf.urls import url

from . import views

app_name = 'euro'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check_login$', views.check_login, name='check_login'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    
    url(r'^logout$', views.logout, name='logout'),
    
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
        

]