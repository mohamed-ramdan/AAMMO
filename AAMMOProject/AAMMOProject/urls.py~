from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('main.urls')),
	url(r'^captcha/', include('captcha.urls')),
	url(r'^article/', include('article.urls')),
	url(r'^comment/', include('comments.urls')),
	url(r'^users/', include('users.urls')),
	url('', include('social.apps.django_app.urls', namespace='social')),
]
