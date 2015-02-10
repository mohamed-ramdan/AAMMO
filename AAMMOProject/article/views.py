from django.shortcuts import render
from django.http import HttpResponse
from article.models import Entity
from article.models import Article

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
	
	# The following steps to sava from template in database in article table	
		article_instance=Article()
		article_instance.article_title=article_title
		article_instance.article_body=article_body
		article_instance.article_photo=photo_path
		article_instance.article_published=article_publish
		article_instance.article_tag=article_tag
		article_instance.entity_id_id=entity_instance.id
		article_instance.save()
		return HttpResponse('hiii')
	except:
		return HttpResponse('NOOO')

	# The try and Exception block to handle the exception from no field is filled 	


# This is function of take the value from data base and put them in template 
def article(request):
	
	entity_instance=Entity.objects.get(id=14)
	article_instance=Article.objects.get(entity_id_id=14)
	context={'entity':entity_instance,'article':article_instance,'flag':1}
	return render(request,'create_article.html',context)

# This is function of editing in the article 	
#search by id and save in database  fadlha bs eni ab3tlha id k paramaeter 

def edit_article(request):
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
		entity_instance=Entity.objects.get(id=14)
		entity_instance.entity_date=article_date
		entity_instance.entity_time=article_time
		entity_instance.entity_type=entity_type
		entity_instance.save()
	
	# The following steps to save what we read from templates in database in article table	
		article_instance=Article.objects.get(entity_id_id=14)
		article_instance.article_title=article_title
		article_instance.article_body=article_body
		article_instance.article_photo=photo_path
		article_instance.article_published=article_publish
		article_instance.article_tag=article_tag
		article_instance.entity_id_id=entity_instance.id
		article_instance.save()
		return HttpResponse('hiii')
	except:
		return HttpResponse('you must enter the paramater')
	
	# The try and Exception block to handle the exception from no field is filled 	


# This is function to delete an article fadl ab3t f paramater id w dh elly 3ml search beh 
def delete_article(request):
	try:
		article=Article.objects.get(entity_id_id=8)
		article.delete()
		instance = Entity.objects.get(id=7)
		instance.delete()
		return HttpResponse('hiii')
	except:
		return HttpResponse('NOOOO')

	#The try and Exception block to handle the exception if the selected article to delete not found




# This is function of take tags 
#fadl ab3t id k parameter
def relate_article(request):
	list1=[]
	# This line to get current Article by id
	article=Article.objects.get(entity_id=17)
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
			
			
		
	context={'tag':list1}
	return render(request,'article.html',context)


