from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'AAMMOProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

     url(r'^createarticle/$','article.views.createarticle'),

     url(r'^home_article/$','article.views.home_article'),

     url(r'^list_articles/$','article.views.list_articles'),

     url(r'^admin_article/$','article.views.admin_article'),

     url(r'^sort_published/$','article.views.sort_published'),

     url(r'^like/(?P<article_id>\d+)/$','article.views.like'),

     url(r'^unlike/(?P<article_id>\d+)/$','article.views.unlike'),

     url(r'^open_article/(?P<article_id>\d+)/$','article.views.open_article')

    #url(r'^details/(?P<question_id>\d+)/$','mytest.views.details'),
]
