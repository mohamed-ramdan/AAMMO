from django.conf.urls import url

urlpatterns = [
	url(r'^register/', 'users.views.register'),
	url(r'^logout/', 'users.views.logout'),
	url(r'^login/', 'users.views.login'),
]
