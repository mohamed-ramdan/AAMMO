from django.conf.urls import include, url

urlpatterns = [
	url(r'^register/', 'users.views.register'),
]
