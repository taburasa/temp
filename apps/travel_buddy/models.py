from __future__ import unicode_literals

from django.db import models
from ..login_registration.models import User, UserManager

# Create your models here.
class TripManager(models.Manager):
    def add_trip(self, form_data):
        destination = form_data['destination']
        description = form_data['description']
        planner = User.objects.get(id=form_data['planner'])
        date_from = form_data['date_from']
        date_to = form_data['date_to']
        trip = Trip.objects.create(planner=planner, destination=destination, description=description, date_from=date_from, date_to=date_to)
        # trip.save()
        return trip

class Trip(models.Model):
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    planner = models.ForeignKey(User, related_name="planned_trips")
    tagalongs = models.ManyToManyField(User, related_name="tagalong_trips")
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

    def __str__(self):
        return self.destination
