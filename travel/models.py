from django.db import models
from datetime import datetime,date
from django import utils


class Destination(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to ='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(False)

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

class Tickets(models.Model):
    flights = models.ForeignKey(Flights,on_delete=models.CASCADE)
    num_seats = models.IntegerField()
    cost = models.IntegerField()


