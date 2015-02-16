from django.conf.urls import url

urlpatterns = [
	url(r'^article/(?P<entity_id>\d+)/$', 'article.views.article'),
	url(r'^home_article/$', 'article.views.home_article'),
	url(r'^list_articles/$', 'article.views.list_articles'),
	url(r'^open_article/(?P<entity_id>\d+)/$', 'article.views.open_article'),
	url(r'^create_article/$', 'article.views.create_article'),
	url(r'^insert_article/$', 'article.views.insert_article'),
	url(r'^delete_article/(?P<entity_id>\d+)/$', 'article.views.delete_article'),
	url(r'^edit_article/(?P<entity_id>\d+)/$', 'article.views.edit_article'),
	url(r'^like/(?P<entity_id>\d+)/$', 'article.views.like'),
	url(r'^unlike/(?P<entity_id>\d+)/$', 'article.views.unlike'),
	url(r'^sort_published/$', 'article.views.sort_published'),
]
