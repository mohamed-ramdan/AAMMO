from PIL import Image
from django.db import models

from django.utils import timezone

from users.models import Users


class Entity(models.Model):
	""" 
	This is the entity's model class. It contains information pertaining to common features between article and
	comments.It`s considered a superclass  model that contain two subclass models(Comments and Articles) .type field
	dedicate the type
	"""

	# The no of like that user made field
	no_of_likes = models.IntegerField(default=0)

	# The Date field either for article or for comment
	entity_date = models.DateField(default=timezone.now)

	# The Time field either for article or for comment
	entity_time = models.TimeField(default=timezone.now)

	# The type field to decide article or comment (type=1 then comment else if type=2 then article)
	entity_type = models.IntegerField(default=0)

	# The author_id field related to admin that created the article
	author_id = models.ForeignKey(Users)


class Article(models.Model):
	"""
	This is the Article's model class. It contains information pertaining to each Article. A Article can also be
	published or not,
	admin only can add article .
	"""
	# The article title field
	article_title = models.CharField(max_length=300)

	# The article description field
	article_body = models.TextField()

	# The photo upload related to article field
	article_photo = models.FileField(upload_to='article_pics/%Y/%m/%d')

	# The article published field (if =1 then published if =0 then not published)
	article_published = models.IntegerField(default=0)

	# The article tag field
	article_tag = models.CharField(max_length=300)

	# The foreign key that make a relation between Entity and Article tables
	entity_id = models.ForeignKey(Entity)

	def save(self):
		"""
		Override the model's save function to resize the photo to 100x100 first.
		:return:
		"""
		super(Article, self).save()

		if self.article_photo:
			image_path = str(self.article_photo.path)
			image_object = Image.open(image_path)

			image_object.thumbnail((600, 600), Image.ANTIALIAS)
			image_object.save(image_path)


class Likes(models.Model):
	"""
	This is Likes to entity model that contains information about the user that like the entity (article/comment)
	"""

	# User_like_id field related to users
	user_like_id = models.ForeignKey(Users)
	# Entity_like_id field related to entity(article/comment)
	entity_like_id = models.ForeignKey(Entity)

