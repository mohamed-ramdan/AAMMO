from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from article.models import Entity,Article

# Create your views here.

# This is function of go to the page of adding new article
def createarticle(request):
	return render(request,'create_article.html')
	



# This is function of adding new Article
def insert_article(request):
	try:    
	# The following to take value from template
		photo_path=request.POST['article_photo']
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

	# The following steps to sava from template in database in entity table
		entity_instance=Entity()
		entity_instance.entity_date=article_date
		entity_instance.entity_time=article_time
		entity_instance.entity_type=entity_type
		entity_instance.save()
	except Exception,e:
		
		return render(request,'create_article.html',{'message':"you must enter all fields "})
	try:
	# The following steps to sava from template in database in article table	
		article_instance=Article()
		article_instance.article_title=article_title
		article_instance.article_body=article_body
		article_instance.article_photo=photo_path
		article_instance.article_published=article_publish
		article_instance.article_tag=article_tag
		article_instance.entity_id_id=entity_instance.id
		article_instance.save()

		return HttpResponseRedirect("http://127.0.0.1:8000/article/admin_article/") 
	except Exception,e:
		
		return render(request,'create_article.html',{'message':"you must enter all field"})

	# The try and Exception block to handle the exception from no field is filled 	


# This is function of take the value from data base and put them in template 
def article(request,article_id):
	article=Article.objects.get(pk=article_id)
	entity_instance=Entity.objects.get(id=article.entity_id_id)
	article_instance=Article.objects.get(entity_id_id=article.entity_id_id)
	context={'entity':entity_instance,'article':article_instance,'flag':1}
	return render(request,'create_article.html',context)

# This is function of editing in the article 	
#search by id and save in database  fadlha bs eni ab3tlha id k paramaeter 

def edit_article(request,article_id):
	try:
	# The following is to read from templates
		photo_path=request.POST['article_photo']
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

	# The following steps to save what we read from templates in database in entity table
		article=Article.objects.get(pk=article_id)
		entity_instance=Entity.objects.get(id=article.entity_id_id)
		entity_instance.entity_date=article_date
		entity_instance.entity_time=article_time
		entity_instance.entity_type=entity_type
		entity_instance.save()
	
	# The following steps to save what we read from templates in database in article table	
		article_instance=Article.objects.get(entity_id_id=article.entity_id_id)
		article_instance.article_title=article_title
		article_instance.article_body=article_body
		article_instance.article_photo=photo_path
		article_instance.article_published=article_publish
		article_instance.article_tag=article_tag
		article_instance.entity_id_id=entity_instance.id
		article_instance.save()
	
		return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(article_id)+"/") 
	except:
		context={'message':"please enter all fields",'entity':entity_instance,'article':article,'flag':1}
		return render(request,'create_article.html',context)
	
	# The try and Exception block to handle the exception from no field is filled 	


# This is function to delete an article 
def delete_article(request,article_id):
	
	article=Article.objects.get(pk=article_id)
	article=Article.objects.get(entity_id_id=article.entity_id_id)
	article.delete()
	instance = Entity.objects.get(id=article.entity_id_id)
	instance.delete()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/admin_article/") 
	


# This function to list articles  limitted by 5 articles "home page"
def home_article(request):
    # select all entites which type=2 that mean it`s article type sorting first by date then by time 
	entities = Entity.objects.filter(entity_type=2).order_by('entity_date', 'entity_time')[:5]
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





# This function to list all articles   "Articles page"
def list_articles(request):
	entities = Entity.objects.filter(entity_type=2).order_by('entity_date', 'entity_time')
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
	return render(request,'articles.html',context)





# This function to select article with it`s  "article page"
def open_article(request,article_id):
	article_data=get_object_or_404(Article,pk=article_id)
	entity=Entity.objects.get(id=article_data.entity_id_id)
	# related tags in article page
	list1=[]
	# This line to get current Article by id
	article=Article.objects.get(entity_id=article_data.entity_id_id)
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

	context={'article':article_data,'entity':entity,'tag':list1}
	return render(request,'article.html',context)






# This function to list articles to admin page and provide his priveladges "admin page"
# Sorted by default by published date 
def admin_article(request):

	# select all entites which type=2 that mean it`s article type sorting first by date then by time 
	entities = Entity.objects.filter(entity_type=2).order_by('entity_date', 'entity_time')
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







# This function to sort the articles even published or not "admin page"
def sort_published(request):
	# select all entites which type=2 that mean it`s article type sorting first by date then by time 
	entities = Entity.objects.filter(entity_type=2).order_by('entity_date', 'entity_time')
	# select all articles sorted by it's published or not
	articles=Article.objects.all().order_by('-article_published')
	context={'articles':articles,'entities':entities}
	return render(request,'admin.html',context)







# This function to increase no of likes when user submit like button "article page"
def like(request,article_id):
	# get article data by it`s id
	article_data=get_object_or_404(Article,pk=article_id)
	# get information of this article from parent Entity
	entity=Entity.objects.get(id=article_data.entity_id_id)
	entity.no_of_likes+=1
	# saving in database
	entity.save()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(article_id)+"/") 






# This function to decrease no of likes when user submit unlike button "article page"
def unlike(request,article_id):
	# get article data by it`s id
	article_data=get_object_or_404(Article,pk=article_id)
	# get information of this article from parent Entity
	entity=Entity.objects.get(id=article_data.entity_id_id)
	if entity.no_of_likes <= 0: 
		entity.no_of_likes=0
	else:
		entity.no_of_likes-=1
	# saving in database
	entity.save()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(article_id)+"/")





