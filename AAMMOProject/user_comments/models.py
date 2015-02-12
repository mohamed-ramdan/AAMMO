from django.db import models

# Comment table / model
class Comment(models.Model):
	# The date comment created in
	created = models.DateTimeField(auto_now_add=True)
	# Comment author 	
	author = models.CharField(max_length=60)
	# Comment body 	
	body = models.TextField()
	# Comment foreign key that pointer the article the comment belong to	
	#article = models.ForeignKey(article)



