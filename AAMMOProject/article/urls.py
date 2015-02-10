from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'AAMMOProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

     url(r'^createarticle/$','article.views.createarticle'),
     url(r'^insert_article/$','article.views.insert_article'),
	 url(r'^delete_article/$','article.views.delete_article'),
	 url(r'^article/$','article.views.article'),
	 url(r'^edit_article/$','article.views.edit_article'),
	 url(r'^relate_article/$','article.views.relate_article'),
    #url(r'^details/(?P<question_id>\d+)/$','mytest.views.details'),
]
