from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect,HttpResponseForbidden
from article.models import Entity,Article,Likes
from users.models import Users
from article.forms import UploadImageForm




def createarticle(request):
	""" This is function of go to the page of adding new article"""
	return render(request,'create_article.html')
	






def insert_article(request):

	""" This is function of adding new Article"""

	
	# The try and Exception block to handle the exception from no field is filled 
	try:    
	# The following to take value from create article page
		article_title=request.POST['article_title']
		article_tag=request.POST['article_tag']
		article_body=request.POST['article_body']
		article_date=request.POST['article_date']
		article_time=request.POST['article_time']

	
	# In the data base article type take number 2 in the entity table
		entity_type=2
		query_list=request.POST.getlist('publish_article')
	
	# This to read the value of checkbox if checked put article_publish=1 if not checked put article_publish=0
		if 'on' in query_list:
			article_publish=1
		else :
			article_publish=0



	# to get user 
		username=request.session['username']
		check_user=Users.objects.get(user_name=username)


	# The following steps to sava from create_article page in database in entity table
		entity_instance=Entity()
		entity_instance.entity_date=article_date
		entity_instance.entity_time=article_time
		entity_instance.entity_type=entity_type
		entity_instance.author_id_id=check_user.user_id
		entity_instance.save()

	except Exception,e:

		return render(request,'create_article.html',{'message':"please enter all fields"})
	try:
	# The following steps to save from create_article page in database in article table
		
		# uploading picture to Article from file or noimage inserted
		article_instance=Article()
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			article_instance.article_photo = form.cleaned_data['image']
		else:
			article_instance.article_photo ="noimage.jpg"

		# cont saving all parameters of article
		article_instance.article_title=article_title
		article_instance.article_body=article_body
		article_instance.article_published=article_publish
		article_instance.article_tag=article_tag
		article_instance.entity_id_id=entity_instance.id
		article_instance.save()
		return HttpResponseRedirect("http://127.0.0.1:8000/article/admin_article/") 
	except Exception,e:
		return render(request,'create_article.html',{'message':"please enter all fields"})

	




def article(request,entity_id):
	""" This is function of take the value from data base and put them in create_article page 
	    with flag=1 that mean it`s in edit mode"""
	
	entity_instance=Entity.objects.get(id=entity_id)
	article_instance=Article.objects.get(entity_id_id=entity_id)
	context={'entity':entity_instance,'article':article_instance,'flag':1}
	return render(request,'create_article.html',context)







	


def edit_article(request,entity_id):
	""" This is function of editing in the article"""


	# The try and Exception block to handle the exception from no field is filled 
	try:
	
	# The following is to read from create_article page
		
		article_title=request.POST['article_title']	
		article_tag=request.POST['article_tag']
		article_body=request.POST['article_body']
		article_date=request.POST['article_date']
		article_time=request.POST['article_time']
		entity_type=2
		

		query_list=request.POST.getlist('publish_article')
		if 'on' in query_list:
			article_publish=1
		else :
			article_publish=0

	# The following steps to save what we read from create_article page in database in entity table
		
		entity_instance=Entity.objects.get(id=entity_id)
		entity_instance.entity_date=article_date
		entity_instance.entity_time=article_time
		entity_instance.entity_type=entity_type
		entity_instance.save()
	

	# The following steps to save what we read from create_article page in database in article table	
		article_instance=Article.objects.get(entity_id_id=entity_id)


		# uploading picture to Article
		form = UploadImageForm(request.POST, request.FILES)
		if form.is_valid():
			article_instance.article_photo = form.cleaned_data['image']
		else:
			article_instance.article_photo ="noimage.jpg"

        # cont saving parameters in database  
		article_instance.article_title=article_title
		article_instance.article_body=article_body
		article_instance.article_published=article_publish
		article_instance.article_tag=article_tag
		article_instance.entity_id_id=entity_instance.id
		article_instance.save()
	
		return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(entity_id)+"/") 
	except:
		context={'message':"please enter all fields",'entity':entity_instance,'article':article,'flag':1}
		return render(request,'create_article.html',context)
	
		






def delete_article(request,entity_id):
	"""This is function to delete an article """
	
	
	article=Article.objects.get(entity_id_id=entity_id)
	article.delete()
	instance = Entity.objects.get(id=entity_id)
	instance.delete()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/admin_article/") 
	





 	
def check(request):
	""" This is a function to check whether login person is admin or user """
	
	# to get user 
	username=request.session['username']
	check_user=Users.objects.get(user_name=username)
	
	
	# Check by attribute admin status 
	if check_user.user_admin_status:

		# If the login person is admin then goto admin page
		return HttpResponseRedirect("http://127.0.0.1:8000/article/admin_article/") 
	else:

		# If the login person is user then goto homw page
		return HttpResponseRedirect("http://127.0.0.1:8000/article/home_article/") 






def home_article(request):

	""" This function to list articles  limitted by 5 articles "home page" """

    # select all entites which type=2 that mean it`s article type sorting first by date then by time 
	entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')[:5]
	#list of articles which saving on it the selected articles
	articles_list=[]
	# for loop that make inner join 
	#get all articles sorted which the forienkey entity_id in article class equal to id of entity class
	for instance  in entities:
		article=Article.objects.get(entity_id=instance.id)
		#append the article in list of articles
		articles_list.append(article)

	#saving entities and articles in dictionary list to render to index.html
	context={'entities': entities,'articles':articles_list}

	return render(request,'index.html',context)









def list_articles(request):

	""" This function to list all articles   "Articles page" """

	entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')
	#list of articles which saving on it the selected articles
	articles_list=[]
	# for loop that make inner join 
	#get all articles sorted which the forienkey entity_id in article class equal to id of entity class
	for instance  in entities:
		article=Article.objects.get(entity_id=instance.id)
		#append the article in list of articles
		articles_list.append(article)


	# to check this user is admin or user
	username=request.session['username']
	user=Users.objects.get(user_name=username)
	
	# check for admin status 
	if user.user_admin_status:
		# admin flag =1 that mean this user is admin
		admin_flag=1
	else:
		admin_flag=0

	#saving entities and articles in dictionary list to render to index.html
	context={'entities': entities,'articles':articles_list,'admin_flag':admin_flag}
	return render(request,'articles.html',context)






def open_article(request,entity_id):

	"""This function to select article with it`s  "article page" """
	
	article_data=get_object_or_404(Article,entity_id=entity_id)
	entity=Entity.objects.get(id=entity_id)
	# related tags in article page
	list1=[]
	# This line to get current Article by id
	article=Article.objects.get(entity_id=entity_id)
	


	# This line to select all from article table
	tags=Article.objects.all()
	# This line to split tag  of current article into list
        current_tag=article.article_tag.split(',')
	# This is for loop to get row by row from Article table
	for tag in tags:
		# This is to split tag of selected row
		selected_tag=tag.article_tag.split(',')
		# This two for loop is to compare word by wo
		for word in selected_tag :
			for current in current_tag:
				# The if statement is to compare selected word from selected tag row  and selected word from current tag  
				if current==word:
					# Append the correct tag in list
					list1.append(tag)
			#Break statement to not repeat the apend 		
			break

	

	# to check this user is admin or user
	username=request.session['username']
	user=Users.objects.get(user_name=username)
	
	# check for admin status 
	if user.user_admin_status:
		# admin flag =1 that mean this user is admin
		admin_flag=1
	else:
		admin_flag=0

	


	# to check even user is liked in this article or not to display like or unlike button
	
	#select all users and it`s articles that making like on it
	all_user=Likes.objects.all()
	
	#flag to decide which display like button or unlike button
	#flag=0 that mean like button is visible
	flag=0
	# for loop to get every user with it`s article
	for current_user in all_user:
		#check if user in table of likes or not
		if current_user.user_like_id_id==3:
			# if current user likes this article or not
			if current_user.entity_like_id_id==article_data.entity_id_id:
				#flag=1 mean unlike button is visible
				flag=1 
				break
	#check the value of flag 
	if flag==1:
		context={'article':article_data,'entity':entity,'tag':list1,'flag':1,'admin_flag':admin_flag}
		
	else:
		context={'article':article_data,'entity':entity,'tag':list1,'flag':0,'admin_flag':admin_flag}
	
	return render(request,'article.html',context)
		




def admin_article(request):
     
	"""  This function to list articles to admin page and provide his priveladges "admin page"
               Sorted by default by published date  """

	# select all entites which type=2 that mean it`s article type sorting first by date then by time 
	entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')
	#list of articles which saving on it the selected articles
	articles_list=[]
	# for loop that make inner join 
	#get all articles sorted which the forienkey entity_id in article class equal to id of entity class
	for instance  in entities:
		article=Article.objects.get(entity_id=instance.id)
		#append the article in list of articles
		articles_list.append(article)

	#saving entities and articles in dictionary list to render to index.html
	context={'entities': entities,'articles':articles_list}

	return render(request,'admin.html',context)








def sort_published(request):

	"""This function to sort the articles even published or not "admin page" """

	# select all entites which type=2 that mean it`s article type sorting first by date then by time 
	entities = Entity.objects.filter(entity_type=2).order_by('-entity_date', '-entity_time')
	# select all articles sorted by it's published or not
	articles=Article.objects.all().order_by('-article_published')
	context={'articles':articles,'entities':entities}
	return render(request,'admin.html',context)








def like(request,entity_id):

	""" This function to increase no of likes when user submit like button "article page" """

	# get article data by it`s id
	article_data=get_object_or_404(Article,entity_id_id=entity_id)
	# get information of this article from parent Entity
	entity=Entity.objects.get(id=entity_id)
	entity.no_of_likes+=1
	# saving in database
	entity.save()

	# to get user id
	username=request.session['username']
	user=Users.objects.get(user_name=username)

	# saving that user likes this article
	like=Likes()
	like.user_like_id_id=user.user_id
	like.entity_like_id_id=entity_id
	like.save()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(entity_id)+"/") 







def unlike(request,entity_id):

	"""This function to decrease no of likes when user submit unlike button "article page" """
	# get article data by it`s id
	article_data=get_object_or_404(Article,entity_id_id=entity_id)
	# get information of this article from parent Entity
	entity=Entity.objects.get(id=entity_id)
	if entity.no_of_likes <= 0: 
		entity.no_of_likes=0
	else:
		entity.no_of_likes-=1
	# saving in database
	entity.save()

	# to get user id
	username=request.session['username']
	user=Users.objects.get(user_name=username)

	# to delete the like of the user on the related article
	all_user=Likes.objects.all()

	# for loop to get every user with it`s article
	for current_user in all_user:
		#check if this user in table of likes or not
		if current_user.user_like_id_id==user.user_id:
			# if current user likes this article or not
			if current_user.entity_like_id_id==article_data.entity_id_id:
				# delete his like
				current_user.delete()

	return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(entity_id)+"/")
	





