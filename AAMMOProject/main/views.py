from django.shortcuts import render


def index(request):
	"""
	This function returns
	:param request:
	:return:
	"""
	return render(request,'index.html')