from django.db import models
from django.contrib.auth.models import Group, User
from .utils.enums import GENDER_CHOICES, BOAT_CHOICES, LOCATION_CHOICES, SIDE_CHOICES, SIDE_BOW, SIDE_STROKE
import datetime
from django.utils import timezone

class Rower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, blank=True) # TODO !!!
    preferred_side = models.CharField(max_length=2, choices=SIDE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_cox = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    wants_organizer_mail = models.BooleanField(default=False)

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Crew(Group):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    members = models.ManyToManyField(Rower, related_name='member_of_crew')
    organizers = models.ManyToManyField(Rower, related_name='organizes_crew')

    def getEvents(self):
        now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        return self.event_set.filter(starting_time__gte = now).order_by('starting_time')

    def getOrganizerMail(self):
        addr = []
        for organizer in self.organizers.all():
            if organizer.wants_organizer_mail:
                addr.append(organizer.user.email)
        return addr

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
                            limit_choices_to={'is_coach':True}, null=True, blank=True, related_name='coxing_in')
    coaches = models.ForeignKey(Rower,on_delete=models.SET_NULL,
                                limit_choices_to={'is_coach':True}, null=True, blank=True,related_name='coaching_in')
    crew = models.ForeignKey(Crew, null=True, blank=True)
    members = models.ManyToManyField(Rower, related_name='rowing_in')
    strokeside = models.ManyToManyField(Rower, related_name='strokeside_in')
    bowside = models.ManyToManyField(Rower, related_name='bowside_in')
    oars = models.ForeignKey(Oars, null=True, blank=True)
    coxBox = models.ForeignKey(CoxBox, null=True, blank=True)
    isRace = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def getJoiniesMail(self):
        mail = []
        for member in self.members.all():
            mail.append(member.user.email)
        if self.cox is not None:
            mail.append(self.cox.user.email)
        if self.coaches is not None:
            mail.append(self.coaches.user.email)
        return mail

    def countBowside(self):
        return self.members.filter(preferred_side=SIDE_BOW).count()

    def countStroke(self):
        return self.members.filter(preferred_side=SIDE_STROKE).count()


    def shouldJoinRowing(self, rower):
        if rower in self.members.filter(rower=rower).exists():
            return "DropOut"
        else:
            return "Join"

    def in_future(self):
        if self.ending_time > timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()):
            return True
        else:
            print(self.ending_time)
            print(timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()))
            return False

    def __str__(self):
        if self.crew is not None:
            return self.crew.name + " - " + self.starting_time.strftime('%Y-%m-%d %H:%M')
        else:
            return self.starting_time.strftime('%Y-%m-%d %H:%M')



class BoatClub(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)
    nickname = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=30, unique=True)



