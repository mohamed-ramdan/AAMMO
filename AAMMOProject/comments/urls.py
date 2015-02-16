from django.conf.urls import url

urlpatterns = [
	url(r'^list_comments/(?P<entity_id>\d+)/$', 'comments.views.list_comments'),
	url(r'^insert_comment/(?P<entity_id>\d+)/$', 'comments.views.insert_comment'),
	url(r'^like/(?P<entity_id>\d+)/$', 'comments.views.like'),
	url(r'^unlike/(?P<entity_id>\d+)/$', 'comments.views.unlike'),
]