from django.core.mail import send_mail
from .constans import EmailPrefix, NoReplyEmail

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