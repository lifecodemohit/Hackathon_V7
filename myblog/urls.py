from django.conf.urls import patterns, url
from myblog import views
from myblog.models import *
urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^logout$', views.signout, name='signout'),
	url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^graph$', views.graph, name='graph'),

    url(r'^add_question$', views.add_question, name='add_question'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^question/(?P<question_id>\d+)/question_upvote/$', views.question_upvote, name='question_upvote'),
)