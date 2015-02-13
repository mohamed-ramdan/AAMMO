from django.shortcuts import render
from article.models import Likes,Entity,Article
from users.models import Users
from comments.models import Comment
from django.http import HttpResponseRedirect
from django.http import HttpResponse

def list_comments(request):
	""" This function to list all comments with it`s replies on the same article """

	#select all comments with type=1 which mean that is comments sorted by date and time 
	entities = Entity.objects.filter(entity_type=1).order_by('-entity_date', '-entity_time')
	#list of comments which saving on it the selected comments
	article_comments_replies_sorted=[]
	# 2 mtched to article_id
	# get all comments and replies of specified article
	article_comments_replies=Comment.objects.filter(article_id_id=2)
	# seprate comments and replies
	for article_comment_reply in article_comments_replies:
		if article_comment_reply.comment_id_id:
			





	# to sort all comments and replies of specified article
	# for loop that make inner join 
	#get all comments sorted which the forienkey entity_id in comment class equal to id of entity class
	for instance  in entities:
		comment=Comment.objects.get(entity_id=instance.id ,comment_id_id__isnull=True)
		#append the comment in list of comments
		comments_list.append(comment)

#saving entities and comments in dictionary list to render to index.html
	context={'entities': entities,'comments':comments_list}
	return render(request,'comments.html',context)




# To goto the page of comemnt to insert comment


def create_comment(request):
	return render(request,'insert_comment.html')
# to save the data into the comment and entitiy table 


def insert_comment(request):
	
	comment_body=request.POST['comment_body']
# to save the data into entity table and make the time and date take the default value
	entity_instance=Entity()
	entity_instance.entity_type=1
	entity_instance.author_id_id=1
	entity_instance.save()
#to save the data into comment table 

	comment_instance=Comment()
	comment_instance.comment_text=comment_body
	comment_instance.article_id_id=2 ##gyaly f request
	comment_instance.entity_id_id=entity_instance.id
	comment_instance.save()
	return HttpResponse("hiii")
	#el mfrod hyrg3 tany l page el article w feha kol el comments w feha mkan ll comment bt3to 

	#return render(request,'insert_comment.html')

#bmgrd m bdos 3 klmt reply bytl3ly el text area de w kaman bytl3lyzrar bt3 save comment
def comment_on_comment(request):
	insertreply=1
	context={'reply':insertreply}
	return render(request,'insert_comment.html',context)

def save_comment_on_comment(request,comment_id):
	
	comment_body=request.POST['reply_comment']
# to save the data into entity table and make the time and date take the default value
	entity_instance=Entity()
	entity_instance.entity_type=1
	entity_instance.author_id_id=1
	entity_instance.save()
#to save the data into comment table 

	comment_instance=Comment()
	comment_instance.comment_text=comment_body
	comment_instance.article_id_id=2 ##gyaly f request
	comment_instance.entity_id_id=entity_instance.id
	comment_instance.comment_id_id=comment_id
	comment_instance.save()
#dh el mfrod yro7 3 sf7t el article bel comments w kda 
	return HttpResponse("hiii")
	

	
	
