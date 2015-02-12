from django.contrib.auth import logout
from django.shortcuts import render
from users.models import Users


def index(request):
	"""
	This function returns
	:param request:
	:return:
	"""

	return render(request, 'index.html')