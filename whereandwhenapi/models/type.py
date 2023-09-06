# Table Type {
#   id int pk
#   type varchar
# }

"""Type class module"""
from django.db import models

class Type(models.Model):
    """Type class"""
    type = models.CharField(max_length=200)
