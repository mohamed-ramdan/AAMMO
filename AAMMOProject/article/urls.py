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

     url(r'^open_article/(?P<article_id>\d+)/$','article.views.open_article'),
    
     url(r'^insert_article/$','article.views.insert_article'),

      url(r'^delete_article/(?P<article_id>\d+)/$','article.views.delete_article'),

	 url(r'^article/(?P<article_id>\d+)/$','article.views.article'),

	 url(r'^edit_article/(?P<article_id>\d+)/$','article.views.edit_article'),



]
