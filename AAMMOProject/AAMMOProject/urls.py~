from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^article/', include('article.urls')),
	url(r'^comment/',include('user_comments.urls')),
	url(r'^submit/$','user_comments.views.submit'),
	url(r'^users/', include('users.urls')),
]
