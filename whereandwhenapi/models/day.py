# Table Day {
#   id int pk
#   day varchar
# }

""""Day class module"""
from django.db import models

class Day(models.Model):
    """Day class"""
    day = models.CharField(max_length=200)
