from distutils.command.upload import upload

from django.db import models
from django.contrib.auth.models import User





# Create your models here.
class BlogModel(models.Model):
    id=models.IntegerField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title  = models.CharField(max_length=250)
    decs = models.TextField(max_length=3050, null=True)
    image = models.ImageField(upload_to = "Blog_img")
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
      
      
