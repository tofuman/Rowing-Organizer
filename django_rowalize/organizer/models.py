from django.db import models
from django.contrib.auth.models import Group, User
from .utils.enums import GENDER_CHOICES, BOAT_CHOICES, LOCATION_CHOICES, SIDE_CHOICES


class Rower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True) # TODO !!!
    preferred_side = models.CharField(max_length=2, choices=SIDE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_cox = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Crew(Group):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    members = models.ManyToManyField(Rower, related_name='member_of_crew')
    organizers = models.ManyToManyField(Rower, related_name='organizes_crew')

    def __str__(self):
        return self.name


class Boat(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    capacity = models.PositiveSmallIntegerField(verbose_name="Number of Rowers")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    rig_type = models.CharField(max_length=1, choices=BOAT_CHOICES, verbose_name="rigging of the boat")
    notes = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)
    requiresCoxBox = models.BooleanField(default=False)

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


class Event(models.Model):
    starting_time = models.DateTimeField("Starting time for the Outing")
    ending_time = models.DateTimeField("Ending time for the Outing")
    boat = models.ForeignKey(Boat, null=True, blank=True)
    cox = models.ForeignKey(Rower, on_delete=models.SET_NULL,
                            limit_choices_to={'is_coach':True},null=True, blank=True, related_name='coxing_in')
    coaches = models.ForeignKey(Rower,on_delete=models.SET_NULL,
                                limit_choices_to={'is_coach':True},null=True, blank=True,related_name='coaching_in')
    crew = models.ForeignKey(Crew, null=True, blank=True)
    members = models.ManyToManyField(Rower, related_name='rowing_in')
    oars = models.ForeignKey(Oars, null=True, blank=True)
    coxBox = models.ForeignKey(CoxBox, null=True, blank=True)
    isRace = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)


    def __str__(self):
        if self.crew is not None:
            return self.crew.name + " - " + self.starting_time.strftime('%Y-%m-%d %H:%M')
        else:
            return self.starting_time.strftime('%Y-%m-%d %H:%M')



class BoatClub(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)
    nickname = models.CharField(max_length=15, unique=True, primary_key=True)
    location = models.CharField(max_length=30, unique=True, primary_key=True)



