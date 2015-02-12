from requests import models, models
from django.db import models
# from app_name.models import User



class Entity(models.Model):
	""" 
	This is the entity's model class. It contains information pertaining to common features between article and comments.
	it`s considered a superclass  model that contain two subclass models(Comments and Articles) .type field dedicate the the type

	"""

	#The no of like that user made field
	no_of_likes=models.IntegerField(default=0)

	#The Date field either for article or for comment
	entity_date=models.DateField()

	#The Time field either for article or for comment
	entity_time=models.TimeField()

	#The type field to decide article or comment (type=1 then comment else if type=2 then article)
	entity_type=models.IntegerField(default=0)

	#author_id=models.ForeignKey(User)


class Article(models.Model):
	"""
	This is the Article's model class. It contains information pertaining to each Article. A Article can also be published or not,
	admin only can add article .
	"""
	#The article title field
	article_title=models.CharField(max_length=300)

	#The article description field
	article_body=models.TextField()

	#The photo upload related to article field
	article_photo= models.FileField(upload_to='static/uploads/article_pics/%Y/%m/%d')

	#The article published field (if =1 then published if =0 then not published)
	article_published=models.IntegerField(default=0)

	#The article tag field
	article_tag=models.CharField(max_length=300)

	#The foreign key that make a relation between Entity and Article tables
	entity_id=models.ForeignKey(Entity)




