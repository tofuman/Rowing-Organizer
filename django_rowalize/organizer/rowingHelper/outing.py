from django.contrib import messages
from django.shortcuts import redirect
import logging

from ..models import Rower
from ..utils.email import formOrganizerEmail, formOutingModifyEmail




def row(event, user, action):
    rower = Rower.objects.get(user=user)
    email = None


    if action == 'stroke':
        event.members.add(rower)
        event.strokeside.add(rower)
        formOrganizerEmail("Strokeside", event, rower)
    elif action == 'bow':
        event.members.add(rower)
        event.bowside.add(rower)
        formOrganizerEmail("BowSide", event, rower)
    elif action == 'row':
        event.members.add(rower)
        formOrganizerEmail("a Seat", event, rower)
    elif action == 'leave' and event.members.filter(user=user).count() > 0:
        event.members.remove(rower)
        if (event.strokeside.filter(user=user).count() > 0):
            event.strokeside.remove(rower)
            formOrganizerEmail("Strokeside", event, rower, False)
        elif (event.bowside.filter(user=user).count() > 0):
            event.bowside.remove(rower)
            formOrganizerEmail("Bowside", event, rower, False)
        else :
            formOrganizerEmail("a Seat", event, rower, False)

    event.save()
    return True

def cox(event, user, action):
    rower = Rower.objects.get(user=user)
    if action == 'join' and event.cox is None:
        event.cox = (rower)
        formOrganizerEmail("a Cox", event, rower)
    elif action == 'leave' and event.cox is not None and event.cox == rower:
        event.cox = None
        formOrganizerEmail("a Cox", event, rower, False)
    # email Organizers!
    event.save()
    return True

def coach(event, user, action):
    rower = Rower.objects.get(user=user)
    if action == 'join' and event.coaches is None:
        event.coaches = (rower)
        formOrganizerEmail("a Coach", event, rower, False)
    elif action == 'leave' and event.coaches is not None and event.coaches == rower:
        event.coaches = None
        formOrganizerEmail("a Coach", event, rower, False)
    # email Organizers!
    event.save()
    return True

def organize(event, user, action):
    rower = Rower.objects.get(user=user)
    if event.crew.organizers.filter(user=user).count() > 0:
        if action == 'confirm':
            event.is_confirmed = True
            event.is_canceled = False
            formOutingModifyEmail(event, True)
            event.save()
        elif action == 'cancel':
            event.is_canceled = True
            event.is_confirmed = False
            formOutingModifyEmail(event, False)
            event.save()


def modify(request, event):
    action = request.GET.get('action')
    typ = request.GET.get('typ')
    user = request.user

    return_val = False
    if typ == 'row':
        return_val = row(event, user, action)
    if typ == 'cox':
        return_val = cox(event, user, action)
    if typ == 'coach':
        return_val = coach(event, user, action)
    if typ == 'organize':
        return_val = organize(event, user, action)

    if action == 'leave':
        messages.error(request, 'Oped Out')
    elif return_val:
        messages.success(request, 'Joint Outing')
    return redirect('/organizer/main/')
