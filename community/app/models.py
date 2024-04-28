from django.db import models
from django.utils.timezone import now
class Community(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    privacy = models.CharField(max_length=10)
    owner = models.CharField(max_length=30)
    description = models.CharField(max_length=300)

class UserCommunityMembership(models.Model):
    objects = None
    username = models.CharField(max_length=30)
    community = models.CharField(max_length=100)
    joined_date = models.DateTimeField(default=now, editable=False)

class DefaultTemplate(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    #photo = models.ImageField(upload_to='images')
    #location = models.FloatField()
    event_date = models.DateTimeField(null=True, blank=True)
    community_name = models.CharField(max_length=100)
    author_username = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=now, editable=False)