from requests import models, models
from django.db import models
from users.models import Users
from article.models import Likes,Entity,Article
# Create your models here.

class Comment (models.Model):
	"""
	This is the comment's model class. It contains information pertaining to each comment. A comment is related to Article .

	"""
	
	#The comment text field
	comment_text=models.TextField()

	#The article id  is a foregin key to Article to dedicate the comment on which article
	article_id=models.ForeignKey(Article)

	#The foreign key that make a relation between Entity and comment tables
	entity_id=models.ForeignKey(Entity)
	
	#The foreign key that make a recurisive relation in table comment and to enable u make comment on comment
	comment_id=models.ForeignKey('self')
