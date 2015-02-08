from requests import models, models
from django.db import models
# from app_name.models import User

class Entity(models.Model):

    no_of_likes=models.IntegerField(default=0)
    entity_date=models.DateField()
    entity_time=models.TimeField()
    entity_type=models.IntegerField(default=0)
    #author_id=models.ForeignKey(User)

class Article(models.Model):
    article_title=models.CharField(max_length=300)
    article_body=models.TextField()
    article_photo=models.CharField(max_length=200)
    article_published=models.IntegerField(default=0)
    article_tag=models.CharField(max_length=300)
    entity_id=models.ForeignKey(Entity)




