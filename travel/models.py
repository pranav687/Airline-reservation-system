from django.db import models
from datetime import datetime,date
from django import utils


class Announcement(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()

class Flights(models.Model):
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.IntegerField()
    departure_date = models.DateField(default=date.today())
    departure_time = models.TimeField(default=utils.timezone.now)
    arrival_time = models.TimeField(default=utils.timezone.now)
    available_seats = models.IntegerField()
    #offer = models.BooleanField(default=False)
    
class Passengers(models.Model):   
    flights = models.ForeignKey(Flights,on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=200)
    passenger_age = models.IntegerField()
    seat_num =  models.IntegerField()
    


