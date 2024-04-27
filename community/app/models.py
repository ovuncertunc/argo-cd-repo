from django.db import models
from django.utils.timezone import now
class Community(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    privacy = models.CharField(max_length=10)
    owner = models.CharField(max_length=30)
    description = models.CharField(max_length=300)

class UserCommunityMembership(models.Model):
    username = models.CharField(max_length=30)
    community = models.CharField(max_length=100)
    joined_date = models.DateTimeField(default=now, editable=False)

class DefaultTemplate(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    #photo = models.ImageField(upload_to='images')
    location = models.FloatField()
    date = models.DateTimeField(default=now, editable=False)
    community_name = models.CharField(max_length=100)
    author_username = models.CharField(max_length=30)