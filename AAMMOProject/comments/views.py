from django.shortcuts import render
from article.models import Likes,Entity,Article
from users.models import Users
from comments.models import Comment
from django.http import HttpResponseRedirect
from django.http import HttpResponse

elements =[] 
depth = -1

def get_children_nodes(element_id):
	"""
	This function gets the children of the given element id
	:param node_id:
	:return:
	"""
	children=Comment.objects.filter(comment_id_id=element_id)
	return children


def traverse_comments(element_id):
	global depth,elements
	
	depth += 1
	children_elements = get_children_nodes(element_id)

	if not children_elements:
		depth -= 1
		return
	else:
		for element in children_elements:

			entity=Entity.objects.get(pk=element.entity_id_id)
			user=Users.objects.get(pk=entity.author_id_id)
			username=user.user_name 

			elements.append(
				{
					'comment': element,
					'depth': depth,
					'entity':entity,
					'username':username
				}
			)

			traverse_comments(element.entity_id)
		depth-=1

def list_comments(request):
	""" This function to list all comments with it`s replies on the same article """

	global elements
	#article_id = "whatever"
	# this is entity id of article 
	
	entity_id=1

	elements =[]
	# DFS the comment tree of the given article id.
	traverse_comments(entity_id)

	# (element-->comment,depth,author,date,time,num_of_likes)
	#elements =[] # NODES GLOBAL

	context = {
		'comments': elements,
	}


	return render(request,'comments.html',context)









def create_comment(request):
	return render(request,'insert_comment.html')


# this function get entity_id
def insert_comment(request):
	
	comment_body=request.POST['comment_body']
# to save the data into entity table and make the time and date take the default value
	entity_instance=Entity()
	# entity_type that represent type of comment
	entity_instance.entity_type=1
	# autor id that will be taken from session
	entity_instance.author_id_id=1
	entity_instance.save()

#to save the data into comment table 

	comment_instance=Comment()
	comment_instance.comment_text=comment_body
	# 1 will be entity_id

	comment_instance.comment_id_id=2 ##gyaly f request
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
	comment_instance.comment_id_id=2 ##gyaly f request
	comment_instance.entity_id_id=entity_instance.id
	
	comment_instance.save()
#dh el mfrod yro7 3 sf7t el article bel comments w kda 
	return HttpResponse("hiii")
	

	
	
