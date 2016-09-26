from django import template
register = template.Library()

@register.filter(name='couldJoinIn')
def couldJoinIn(Event, rower):
    return not ( Event.members.filter(user=rower.user).count() > 0 or
                 (Event.cox is not None and Event.cox.user.id is rower.user.id) or
                 (Event.coaches is not None and Event.coaches.user.id is rower.user.id))

@register.filter(name='isRowIn')
def isRowIn(Event, rower):
    return Event.members.filter(user=rower.user).count() > 0

@register.filter(name='isCoxIn')
def isCoxIn(Event, rower):
    return (Event.cox is not None and Event.cox.user.id is rower.user.id)

@register.filter(name='isCoachIn')
def isCoachIn(Event, rower):
    return (Event.coaches is not None and Event.coaches.user.id is rower.user.id)
