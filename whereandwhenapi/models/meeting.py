# Table Meeting {
#   id int pk
#   wso_id int
#   district_id int [ref: > District.id]
#   area_id int [ref: > Area.id]
#   meeting_name varchar
#   start_time time
#   street_address varchar
#   city varchar
#   zip int
#   location_details varchar
#   type_id int [ref: > Type.id]
#   zoom_login int
#   zoom_pass int
#   email varchar
#   phone varchar
#   last_updated timestamp
# }

"""Meeting class module"""
from django.db import models

class Meeting(models.Model):
    wso_id = models.IntegerField()
    district = models.ForeignKey("District", on_delete=models.CASCADE)
    area = models.ForeignKey("Area", on_delete=models.CASCADE)
    meeting_name = models.CharField(max_length=200)
    start_time = models.TimeField()
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip = models.IntegerField()
    location_details = models.CharField(max_length=200)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    zoom_login = models.IntegerField(null=True)
    zoom_pass = models.IntegerField(null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200,null=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    days = models.ManyToManyField("Day", through="MeetingDay", related_name="meetings")
    group_reps = models.ManyToManyField("GroupRep", through="GroupRepMeeting", related_name="meetings")
