from django.db import models

class OvuncTable(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()