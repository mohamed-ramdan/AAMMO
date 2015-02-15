from django.db import models

from users.models import Users

from article.models import Likes, Entity, Article


class Comment(models.Model):
	"""
	This is the comment's model class. It contains information pertaining to each comment.
	A comment is related to Article .
	"""

	# The comment text field
	comment_text = models.TextField()

	# The foreign key references to Entity that describe the type is comment represent child
	entity_id = models.ForeignKey(Entity, related_name="home_set")

	# The foreign key references to Entity describe that comment on comment or on article represent parent
	comment_id = models.ForeignKey(Entity, related_name="away_set")
