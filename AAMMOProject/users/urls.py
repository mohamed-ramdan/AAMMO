from django.conf.urls import include, url

urlpatterns = [
	url(r'^register/', 'users.views.register'),
	url(r'^logout/', 'users.views.logout'),
	url(r'^login/', 'users.views.login'),
]
