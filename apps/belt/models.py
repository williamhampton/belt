from __future__ import unicode_literals

from django.db import models

class users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(blank=True, null=True)

class quotes(models.Model):
    user = models.ForeignKey('users')
    quote = models.CharField(max_length = 1000)
    quoteby = models.CharField(max_length=45, default ='Unkown')

class favorites(models.Model):
    user = models.ForeignKey('users')
    quote = models.CharField(max_length = 1000)
    quoteby = models.CharField(max_length=45, default = 'Unkown')
