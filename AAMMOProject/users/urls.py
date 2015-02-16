from django.conf.urls import url

urlpatterns = [
	url(r'^register/', 'users.views.register'),
	url(r'^logout/', 'users.views.logout'),
	url(r'^login/', 'users.views.login'),
	url(r'^login_facebook/', 'users.views.login_facebook'),
	url(r'^password_recovery/', 'users.views.recover_password'),
	url(r'^edit/', 'users.views.edit'),
	url(r'^list_users/', 'users.views.list_users'),
	url(r'^delete_user/(?P<user_id>\d+)/$', 'users.views.delete_user'),
]
