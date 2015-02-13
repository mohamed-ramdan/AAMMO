from django.shortcuts import render, get_object_or_404, redirect

from article.models import Entity, Article, Likes
from users.models import Users
from article.forms import UploadImageForm


def create_article(request):
	""" This is function of go to the page of adding new article"""
	return render(request, 'create_article.html')


def insert_article(request):
	""" This is the function of adding new Article"""

	# The try and Exception block to handle the exception from no field is filled 
	try:
		# The following to take value from create article page
		article_title = request.POST['article_title']
		article_tag = request.POST['article_tag']
		article_body = request.POST['article_body']
		article_date = request.POST['article_date']
		article_time = request.POST['article_time']

		# In the data base article type take number 2 in the entity table
		entity_type = 2
		query_list = request.POST.getlist('publish_article')

		# This to read the value of checkbox if checked put article_publish=1 if not checked put article_publish=0
		if 'on' in query_list:
			article_publish = 1
		else:
			article_publish = 0

		# To get user id, get the currently logged username and query the database for the id.
		username = request.session['username']
		check_user = Users.objects.get(user_name=username)

		# The following steps save the Create Article form in database in entity table.
		entity_instance = Entity()
		entity_instance.entity_date = article_date
		entity_instance.entity_time = article_time
		entity_instance.entity_type = entity_type
		entity_instance.author_id_id = check_user.user_id
		entity_instance.save()

	except Exception, e:
		return render(request, 'create_article.html', {'message': "Please enter all fields!"})

	try:
		# The following steps to save from create_article page in database in article table

		# Upload picture to Article from file or no image inserted
		article_instance = Article()
		form = UploadImageForm(request.POST, request.FILES)

		# Check if the form is valid
		if form.is_valid():
			# Save the photo and change the photo's name to the a_article_id
			article_instance.article_photo = form.cleaned_data['image']
			image_extension = article_instance.article_photo.name.split('.')[1]
			article_instance.article_photo.name = "a_" + str(entity_instance.id) + '.' + image_extension
		else:
			article_instance.article_photo = "noimage.jpg"

		# Continue saving all parameters of article
		article_instance.article_title = article_title
		article_instance.article_body = article_body
		article_instance.article_published = article_publish
		article_instance.article_tag = article_tag
		article_instance.entity_id_id = entity_instance.id
		article_instance.save()

		return redirect("article/home_article/")

	except Exception, e:
		return render(request, 'create_article.html', {'message': "Please enter all fields!"})


def article(request, entity_id):
	""" This is function of take the value from data base and put them in create_article page 
		with edit_mode = 1 that mean it`s in edit mode"""

	entity_instance = Entity.objects.get(id=entity_id)
	article_instance = Article.objects.get(entity_id_id=entity_id)
	context = {'entity': entity_instance, 'article': article_instance, 'edit_mode': 1}

	return render(request, 'create_article.html', context)


def edit_article(request, entity_id):
	"""
	This function performs editing of the article
	"""

	# The try and Exception block to handle the exception from fields being not filled
	try:
		# The following is to read from create_article page
		article_title = request.POST['article_title']
		article_tag = request.POST['article_tag']
		article_body = request.POST['article_body']
		article_date = request.POST['article_date']
		article_time = request.POST['article_time']
		entity_type = 2

		query_list = request.POST.getlist('publish_article')
		if 'on' in query_list:
			article_publish = 1
		else:
			article_publish = 0

		# The following steps to save what we read from create_article page in database in entity table
		entity_instance = Entity.objects.get(id=entity_id)
		entity_instance.entity_date = article_date
		entity_instance.entity_time = article_time
		entity_instance.entity_type = entity_type
		entity_instance.save()

		# The following steps to save what we read from create_article page in database in article table
		article_instance = Article.objects.get(entity_id_id=entity_id)

		# The following steps to save what we read from create_article page in database in article table
		article_instance = Article.objects.get(entity_id_id=article.entity_id_id)

		# Uploading picture to Article
		form = UploadImageForm(request.POST, request.FILES)

		if form.is_valid():
			# Save the photo and change the photo's name to the a_article_id
			article_instance.article_photo = form.cleaned_data['image']
			image_extension = article_instance.article_photo.name.split('.')[1]
			article_instance.article_photo.name = "a_" + str(entity_instance.id) + '.' + image_extension
		else:
			article_instance.article_photo = "noimage.jpg"

		# Continue saving parameters in database
		article_instance.article_title = article_title
		article_instance.article_body = article_body
		article_instance.article_published = article_publish
		article_instance.article_tag = article_tag
		article_instance.entity_id_id = entity_instance.id
		article_instance.save()

		return redirect("article/open_article/" + str(entity_id) + "/")

	except:
		context = {'message': "Please enter all fields!", 'entity': entity_instance, 'article': article, 'edit_mode': 1}
		return render(request, 'create_article.html', context)


def delete_article(request, entity_id):
	"""
	This function is to delete an article
	"""

	# Get the article that points to the correct entity ID.
	article = Article.objects.get(entity_id_id=entity_id)
	article.delete()
	instance = Entity.objects.get(id=entity_id)
	instance.delete()

	return redirect("article/home_article/")


def home_article(request):
	"""
	This function lists articles limited by 5 articles if the user is not an admin an all if he is. --> "home page"
	"""

	# Check if the is_admin session variable is not set, then the user is a regular user. Get only 5 articles
	if 'is_admin' not in request.session:
		# Select all entities which type=2 that mean it`s article type sorting first by date then by time
		entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')[:5]

	# The user is an admin, get all the articles.
	else:
		entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')

	# List of articles which saving on it the selected articles
	articles_list = []

	# For loop that make inner join
	# Get all articles sorted which the foreign key entity_id in article class equal to id of entity class
	for instance in entities:
		article = Article.objects.get(entity_id=instance.id)
		# Append the article in list of articles
		articles_list.append(article)

	# Saving entities and articles in dictionary list to render to index.html
	context = {'entities': entities, 'articles': articles_list}

	# Reroute to the appropriate page based on whether the user is an admin or not.
	if 'is_admin' not in request.session:
		return render(request, 'index.html', context)
	else:
		return render(request, 'admin.html', context)


def list_articles(request):
	"""
	This function lists all articles --> "Articles page"
	"""

	entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')
	# list of articles which saving on it the selected articles
	articles_list = []
	# For loop that makes inner join
	# Get all articles sorted which the foreign key entity_id in article class equal to id of entity class
	for instance in entities:
		article = Article.objects.get(entity_id=instance.id)

		# Append the article in list of articles
		articles_list.append(article)

	# Saving entities and articles in dictionary list to render to index.html
	context = {'entities': entities, 'articles': articles_list}

	return render(request, 'articles.html', context)


def open_article(request, entity_id):
	"""
	This function to select article with it`s "Article page"
	"""

	article_data = get_object_or_404(Article, entity_id=entity_id)
	entity = Entity.objects.get(id=entity_id)

	# Related tags in article page
	list1 = []

	# This line to get current Article by id
	article = Article.objects.get(entity_id=entity_id)

	# This line to select all from article table
	tags = Article.objects.all()
	# This line to split tag  of current article into list
	current_tag = article.article_tag.split(',')
	# This is for loop to get row by row from Article table
	for tag in tags:
		# This is to split tag of selected row
		selected_tag = tag.article_tag.split(',')
		# This two for loop is to compare word by wo
		for word in selected_tag:
			for current in current_tag:
				# The if statement is to compare selected word from selected tag row and selected word from current tag
				if current == word:
					# Append the correct tag in list
					list1.append(tag)
			# Break statement to not repeat the append
			break

	# To check even user is liked in this article or not to display like or unlike button
	# Select all users and it`s articles that making like on it
	all_user = Likes.objects.all()

	# A like_hidden Flag to decide which display like button or unlike button, like_hidden = 0 that means that the like
	# button is visible
	like_hidden = 0

	# For loop to get every user with it`s article
	for current_user in all_user:
		# Check if user in table of likes or not
		if current_user.user_like_id_id == 3:
			# If current user likes this article or not
			if current_user.entity_like_id_id == article_data.entity_id_id:
				# Flag = 1 mean unlike button is visible
				like_hidden = 1
				break

	# Check the value of like_hidden
	if like_hidden == 1:
		context = {'article': article_data, 'entity': entity, 'tag': list1, 'like_hidden': like_hidden}
	else:
		context = {'article': article_data, 'entity': entity, 'tag': list1, 'like_hidden': like_hidden}

	return render(request, 'article.html', context)


def sort_published(request):
	"""
	This function sorts the articles whether they are published or not in the "Admin Page"
	"""

	# Select all entities which type=2 that mean it`s article type sorting first by date then by time
	entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')

	# Select all articles sorted by it's published or not
	articles = Article.objects.all().order_by('-article_published')

	context = {'articles': articles, 'entities': entities}

	return render(request, 'admin.html', context)


def like(request, entity_id):
	"""
	This function increases the no of likes when user clicks the Like button "Article page"
	"""

	# Get article data by it`s id
	article_data = get_object_or_404(Article, entity_id_id=entity_id)
	# Get information of this article from parent Entity
	entity = Entity.objects.get(id=entity_id)
	entity.no_of_likes += 1
	# Saving in database
	entity.save()

	# To get user id, get the currently logged username and query the database for the id.
	logged_username = request.session['username']
	user_object = Users.objects.get(user_name=logged_username)

	# Saving that user likes this article
	like_object = Likes()
	like_object.user_like_id_id = user_object.user_id
	like_object.entity_like_id_id = entity_id
	like_object.save()

	return redirect("article/open_article/" + str(entity_id) + "/")


def unlike(request, entity_id):
	"""
	This function decreases the no of likes when user submit unlike button "article page"
	"""
	# Get article data by it`s id
	article_data = get_object_or_404(Article, entity_id_id=entity_id)
	# Get information of this article from parent Entity
	entity = Entity.objects.get(id=entity_id)

	if entity.no_of_likes <= 0:
		entity.no_of_likes = 0
	else:
		entity.no_of_likes -= 1

	# Saving in database
	entity.save()

	# To get user id, get the currently logged username and query the database for the id.
	username = request.session['username']
	user = Users.objects.get(user_name=username)

	# To delete the like of the user on the related article
	all_user = Likes.objects.all()

	# For loop to get every user with it`s article
	for current_user in all_user:
		# Check if this user in table of likes or not
		if current_user.user_like_id_id == user.user_id:
			# If current user likes this article or not
			if current_user.entity_like_id_id == article_data.entity_id_id:
				# Delete his like
				current_user.delete()

	return redirect("article/open_article/" + str(entity_id) + "/")
	





