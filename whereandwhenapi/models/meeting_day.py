# Table MeetingDay {
#   id int pk
#   meeting_id int [ref: > Meeting.id]
#   day_id int [ref: > Day.id]
# }

"""MeetingDay class module"""
from django.db import models

class MeetingDay(models.Model):
    """MeetingDay class"""
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    day = models.ForeignKey("Day", on_delete=models.CASCADE)
