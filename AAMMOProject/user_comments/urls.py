from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'AAMMOProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create_comment/$','user_comments.views.create_comment'),
    url(r'^show_comments/$','user_comments.views.show_comments')

]
