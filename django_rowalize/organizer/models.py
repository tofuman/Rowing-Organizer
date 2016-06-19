from django.db import models
from django.contrib.auth.models import User, Group

from .utils.enums import GENDER_CHOICES, BOAT_CHOICES, LOCATION_CHOICES, SIDE_CHOICES


class Coxes(Group):
    pass


class Rowers(Group):
    pass


class BoatOrganizer(Group):
    pass


class Crew(Group):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.nickname


class Rower(models.Model):
    phone_number = models.CharField(max_length=20, blank=True) # TODO !!!
    preferred_side = models.CharField(max_length=2, choices=SIDE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizing = models.ManyToManyField(Crew, blank=True)
    def __str__(self):
        return self.user.username


class Boat(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    capacity = models.PositiveSmallIntegerField(verbose_name="Number of Rowers")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    rig_type = models.CharField(max_length=1, choices=BOAT_CHOICES, verbose_name="rigging of the boat")
    notes = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    def __str__(self):
        return self.name


class Oars(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    number = models.PositiveSmallIntegerField(verbose_name="Number of Oars")
    notes = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    def __str__(self):
        return self.name


class CoxBox(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    notes = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    def __str__(self):
        return self.name


class Outing(models.Model):
    starting_time = models.DateTimeField("Starting time for the Outing")
    ending_time = models.DateTimeField("Ending time for the Outing")
    boat = models.ForeignKey(Boat, null=True, blank=True)
    cox = models.ForeignKey(Rower, null=True, blank=True)
    crew = models.ForeignKey(Crew, null=True, blank=True)
    oars = models.ForeignKey(Oars, null=True, blank=True)
    coxBox = models.ForeignKey(CoxBox, null=True, blank=True)





