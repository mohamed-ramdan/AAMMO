from django.conf.urls import url

urlpatterns = [
	url(r'^register/', 'users.views.register'),
	url(r'^logout/', 'users.views.logout'),
	url(r'^login/', 'users.views.login'),
	url(r'^password_recovery/', 'users.views.recover_password'),
	url(r'^edit/', 'users.views.login'),
	url(r'^edit_success/', 'users.views.login'),
]
