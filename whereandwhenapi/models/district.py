# Table District {
#   id int pk
#   district_number varchar
#   rep_name varchar
# }

"""District class module"""
from django.db import models

class District(models.Model):
    """District class"""
    district_number = models.CharField(max_length=200)
    rep_name = models.CharField(max_length=200)
