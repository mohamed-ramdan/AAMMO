from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from user_comments.models import Comment
# Create your views here.
def show_comments(request):
	comments = Comment.objects.all().order_by('created')
	context={'comments':comments}
	return render(request,'show_comments.html',context)

def create_comment(request):
	return render(request,'comment.html')

def submit(request):
	selected_comment =request.POST['body']
	selected_author=request.POST['author']
	comment= Comment()
	comment.body=selected_comment
	comment.author=selected_author
	comment.save()
	return render(request,'index.html')

