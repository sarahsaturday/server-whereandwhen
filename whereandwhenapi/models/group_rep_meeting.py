# Table GroupRepMeeting {
#   id int pk
#   group_rep_id int [ref: > GroupRep.id]
#   meeting_id int [ref: > Meeting.id]
#   is_home_group bool
# }

"""GroupRepMeeting class module"""
from django.db import models

class GroupRepMeeting(models.Model):
    """GroupRepMeeting class"""
    group_rep = models.ForeignKey("GroupRep", on_delete=models.CASCADE)
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    is_home_group = models.BooleanField(null=True)
