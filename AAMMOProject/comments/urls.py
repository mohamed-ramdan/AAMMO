from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^$', 'AAMMOProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
     url(r'^list_comments/$','comments.views.list_comments'),
     url(r'^create_comment/$','comments.views.create_comment'),
     #url(r'^insert_comment/$','comments.views.insert_comment'),
     url(r'^comment_on_comment/$','comments.views.comment_on_comment'),
        
     url(r'^insert_comment/(?P<entity_id>\d+)/$','comments.views.insert_comment'),
     url(r'^like/(?P<entity_id>\d+)/$','comments.views.like'),
     url(r'^unlike/(?P<entity_id>\d+)/$','comments.views.unlike'),


]
