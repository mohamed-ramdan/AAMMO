from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from article.models import Entity,Article


 

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
	article_data = get_object_or_404(Article,pk=article_id)
	entity=Entity.objects.get(id=article_id)
	context={'article':article_data,'entity':entity}
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
	article_data = get_object_or_404(Article,pk=article_id)
	# get information of this article from parent Entity
	entity=Entity.objects.get(id=article_id)
	entity.no_of_likes+=1
	# saving in database
	entity.save()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(article_id)+"/") 






# This function to decrease no of likes when user submit unlike button "article page"
def unlike(request,article_id):
	# get article data by it`s id
	article_data = get_object_or_404(Article,pk=article_id)
	# get information of this article from parent Entity
	entity=Entity.objects.get(id=article_id)
	if entity.no_of_likes <= 0: 
		entity.no_of_likes=0
	else:
		entity.no_of_likes-=1
	# saving in database
	entity.save()
	return HttpResponseRedirect("http://127.0.0.1:8000/article/open_article/"+str(article_id)+"/")





