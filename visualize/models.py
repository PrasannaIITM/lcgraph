from django.db import models

# Create your models here.
class username(models.Model):
    name = models.CharField(max_length=220)