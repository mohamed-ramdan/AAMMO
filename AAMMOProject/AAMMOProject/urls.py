from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^article/', include('article.urls')),
	url(r'^users/', include('users.urls')),
]
