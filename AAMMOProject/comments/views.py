from django.shortcuts import render,redirect, get_object_or_404
from article.models import Likes, Entity, Article
from users.models import Users
from comments.models import Comment
from django.http import HttpResponseRedirect
from django.http import HttpResponse

elements = []
depth = -1


def get_children_nodes(element_id):
	"""
	This function gets the children of the given element id
	:param node_id:
	:return:
	"""
	children = Comment.objects.filter(comment_id_id=element_id)
	return children


def traverse_comments(element_id):
	global depth, elements

	depth += 1
	children_elements = get_children_nodes(element_id)

	if not children_elements:
		depth -= 1
		return
	else:
		for element in children_elements:
			entity = Entity.objects.get(pk=element.entity_id_id)
			user = Users.objects.get(pk=entity.author_id_id)
			username = user.user_name
			 #To check even user is liked in this comment or not to display like or unlike button
			# Select all users and it`s comments that making like on it
			all_user = Likes.objects.all()
			#A like_hidden Flag to decide which display like button or unlike button, like_hidden = 0 that means that the like
			# button is visible
			like_hidden = 0

			#if 'username' in request.session:
				# # To get user id, get the currently logged username and query the database for the id.
				# logged_username = request.session['username']
				# logged_user = Users.objects.get(user_name=logged_username)
				# For loop to get every user with it`s comment
			for current_user in all_user:
				# Check if user in table of likes or not
				#if current_user.user_like_id_id == logged_user.user_id:
				if current_user.user_like_id_id == 1:
					# If current user likes this comment or not
					if current_user.entity_like_id_id == element.entity_id_id:
						# Flag = 1 mean unlike button is visible
						like_hidden = 1
						break

			


			elements.append(
				{
					'comment': element,
					'depth': depth,
					'entity': entity,
					'username': username,
					'like_hidden':like_hidden
				}
			)

			traverse_comments(element.entity_id)
		depth -= 1


def list_comments(request):
	""" This function to list all comments with it`s replies on the same article """

	global elements
	# article_id = "whatever"
	# this is entity id of article 

	entity_id = 1

	elements = []
	# DFS the comment tree of the given article id.
	traverse_comments(entity_id)


	context = {
		'comments': elements,
	}

	return render(request, 'comments.html', context)


def create_comment(request):
	return render(request, 'insert_comment.html')


# this function get entity_id
def insert_comment(request,entity_id):
	comment_body = request.POST['comment_body']
	# To save the data into entity table and make the time and date take the default value
	entity_instance = Entity()
	# Entity_type that represent type of comment
	entity_instance.entity_type = 1
	# Author id that will be taken from session
	entity_instance.author_id_id = 1
	entity_instance.save()

	# To save the data into comment table

	comment_instance = Comment()
	comment_instance.comment_text = comment_body
	# 1 will be entity_id

	comment_instance.comment_id_id = entity_id ##gyaly f request
	comment_instance.entity_id_id = entity_instance.id
	comment_instance.save()
	#return redirect("/comment/list_comments/" )
	return HttpResponseRedirect("http://127.0.0.1:8000/comment/list_comments/") 





def like(request, entity_id):
	"""
	This function increases the no of likes when user clicks the Like button "comments page"
	"""

	# Get comment data by it`s id
	comment_data = get_object_or_404(Comment, entity_id_id=entity_id)
	# Get information of this article from parent Entity
	entity = Entity.objects.get(id=entity_id)
	entity.no_of_likes += 1
	# Saving in database
	entity.save()

	# To get user id, get the currently logged username and query the database for the id.
	#logged_username = request.session['username']
	#user_object = Users.objects.get(user_name=logged_username)


	# Saving that user likes this comment
	like_object = Likes()
	#like_object.user_like_id_id = user_object.user_id
	like_object.user_like_id_id = 1
	like_object.entity_like_id_id = entity_id
	like_object.save()

	#return redirect("/comment/list_comments/" )
	return HttpResponseRedirect("http://127.0.0.1:8000/comment/list_comments/")





def unlike(request, entity_id):
	"""
	This function decreases the no of likes when user submit unlike button "comments page"
	"""
	# Get comment data by it`s id
	comment_data = get_object_or_404(Comment, entity_id_id=entity_id)
	# Get information of this comment from parent Entity
	entity = Entity.objects.get(id=entity_id)

	if entity.no_of_likes <= 0:
		entity.no_of_likes = 0
	else:
		entity.no_of_likes -= 1

	# Saving in database
	entity.save()

	# To get user id, get the currently logged username and query the database for the id.
	# username = request.session['username']
	# user = Users.objects.get(user_name=username)

	# To delete the like of the user on the related comment
	all_user = Likes.objects.all()

	# For loop to get every user with it`s comment
	for current_user in all_user:
		# Check if this user in table of likes or not
		#if current_user.user_like_id_id == user.user_id:
		if current_user.user_like_id_id == 1:
			# If current user likes this comment or not
			if current_user.entity_like_id_id == comment_data.entity_id_id:
				# Delete his like
				current_user.delete()

	#return redirect("/comment/list_comments/" )
	return HttpResponseRedirect("http://127.0.0.1:8000/comment/list_comments/")






