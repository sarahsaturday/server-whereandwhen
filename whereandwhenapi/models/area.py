# Table Area {
#   id int pk
#   area_number varchar
#   rep_first_name varchar
#   rep_last_name varchar
#   rep_phone varchar
#   rep_email varchar
# }

"""Area class module"""
from django.db import models

class Area(models.Model):
    """Area class"""
    area_number = models.CharField(max_length=200)
    rep_first_name = models.CharField(max_length=200)
    rep_last_name = models.CharField(max_length=200)
    rep_phone = models.CharField(max_length=200)
    rep_email = models.CharField(max_length=200)
