from django.db import models

# Create your models here.
class Post(models.Model):
    年表作成ワード = models.CharField(max_length=200)
    項目数 = models.CharField(max_length=200)
