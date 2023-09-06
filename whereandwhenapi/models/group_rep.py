# Table GroupRep {
#   id int pk
#   user_id int [ref: - User.id]
#   is_group_rep bool
#   is_isr bool
#   phone varchar
# }

"""GroupRep class module"""
from django.db import models
from django.contrib.auth.models import User

class GroupRep(models.Model):
    """GroupRep class"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_group_rep = models.BooleanField()
    is_isr = models.BooleanField()
    phone = models.CharField(max_length=200)
