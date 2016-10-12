from django.core.mail import send_mail
from .constans import EmailPrefix, NoReplyEmail
import logging

class Email():
    def __init__(self, to, subject, sender=None):
        self.to = to
        self.subject = EmailPrefix + subject
        if sender is not None:
            self.sender = sender
        else:
            self.sender = NoReplyEmail

    def send(self, body):
        send_mail(self.subject, body, self.sender, self.to, fail_silently=False)
        logging.info("Send Email to "+ str(self.to))

def formOutingModifyEmail(event, confirm=True):
    if confirm:
        action_string = "CONFIRMED"
    else:
        action_string = "CANCELED"
    email = Email(event.getJoiniesMail(), " Crew " +
                  event.crew.name + " Outing " + str(event.starting_time)+
                  " was "+ action_string)
    if confirm:
        if event.cox is None:
            cox = "No"
        else:
            cox = event.cox.fullname()
        if event.coaches is None:
            coach = "No"
        else:
            coach = event.coaches.fullname()
        names = ""
        for rower in event.members.all():
            names = names + rower.fullname() + "\n"

        body = \
"""Dear Rowers,

The %s outing  has:
%s cox
%s coach
%u rowers (Stroke %u, Bow %u)
%s
The %s has with Cox Box %s and Blades %s will be used.

Thanks,
The System
        """ % (str(event.starting_time),
               cox, coach, event.members.count(), event.strokeside.count(), event.bowside.count(),
               names,
               event.boat.name, event.coxBox.name, event.oars.name)
    else:
        body = "Dear Rowers,\n\nSadly the outing had be canceled.\nThanks,\nThe System"
    try:
        email.send(body)
    except Exception as e:
        logging.error("Send Email Failed!" + str(e))



def formOrganizerEmail(side, event, rower, join=True):
    if join:
        action_string = "Join"
    else:
        action_string = "Drop Out"
    email = Email(event.crew.getOrganizerMail(), " Crew " +
                  event.crew.name + " " + action_string + " of " + rower.fullname() + " for " +
                  side + " (" + str(event.starting_time))
    if event.cox is None:
        cox = "No"
    else:
        cox = event.cox.fullname()
    if event.coaches is None:
        coach = "No"
    else:
        coach = event.coaches.fullname()
    try:
        email.send("""Hello Organizers,

The %s outing now has:
%u rowers (Stroke %u, Bow %u)
%s cox
%s coach
The boat has %u seats, meaning that %u more rowers are needed.

Thanks,
The System
        """ % (str(event.starting_time), event.members.count(), event.strokeside.count(), event.bowside.count(),
                cox, coach,
               event.boat.capacity, (event.boat.capacity - event.members.count())))
    except Exception as e:
        logging.error("Send Email Failed!" + str(e))
