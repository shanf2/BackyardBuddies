from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.JSONField(default = dict)
    
class Dwelling(models.Model):
    address = models.CharField(max_length=150)
    location = models.JSONField(default = dict)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="owner")
    residents = models.ManyToManyField(User)
    description = models.TextField()
