import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
from .utils.enums import GENDER_CHOICES, EnumField, BOAT_CHOICES, LOCATION_CHOICES, SIDE_CHOICES

from django.contrib.auth.models import User


class Rower(models.Model):
    phone_numer = models.CharField(max_length=20) # TODO !!!
    preferred_side = EnumField(choices=SIDE_CHOICES)
    gender = EnumField(choices=GENDER_CHOICES)
    user = models.OneToOneField(User)


class Boat(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    capacity = models.PositiveSmallIntegerField(verbose_name="Number of Rowers")
    gender = EnumField(choices=GENDER_CHOICES)
    rig_type = EnumField(choices=BOAT_CHOICES, verbose_name="rigging of the boat")
    notes = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = EnumField(choices=LOCATION_CHOICES)


class Oars(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    gender = EnumField(choices=GENDER_CHOICES)
    number = models.PositiveSmallIntegerField(verbose_name="Number of Oars")
    notes = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = EnumField(choices=LOCATION_CHOICES)


class CoxBox(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    notes = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = EnumField(choices=LOCATION_CHOICES)


class Outing(models.Model):
    starting_time = models.DateTimeField("Starting time for the Outing")
    ending_time = models.DateTimeField("Ending time for the Outing")
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    cox = 'TBD'
    crew = 'TBD'
    organizer = 'TBD'
    oars = models.ManyToOneRel(Oars)
    coxBox = models.ManyToManyRel(CoxBox)