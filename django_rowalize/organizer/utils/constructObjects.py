from organizer.models import User,Rower, Event, Crew
from django.db.utils import IntegrityError
from django.contrib import messages
from django.core.mail import send_mail

from organizer.utils.constans import NoReplyEmail, AdminEmail, RequestEmail
from organizer.utils.email import Email

def construct_rower(request, form):
    user = None
    rower = None
    try:
        user = User.objects.create_user(form.cleaned_data['username'],
                                        form.cleaned_data['email'],
                                        form.cleaned_data['password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['sir_name'],
                                        is_active=False)
        phone_number = form.cleaned_data['phone_number']
        preferred_side = form.cleaned_data['preferred_side']
        gender = form.cleaned_data['gender']
        is_cox = form.cleaned_data['is_cox']
        is_coach = form.cleaned_data['is_coach']
        rower = Rower(user=user, phone_number=phone_number, preferred_side=preferred_side, gender=gender, is_coach=is_coach,
                      is_cox=is_cox)
        try:
            email = Email([form.cleaned_data['email']], 'Rowing Organizer Account Creation')
            email.send('Thank you for Creating a Account with us '+ form.cleaned_data['username']+'.\n'+\
                                 'Once your account has been activated by an admin you will be able to log in.\n\nKind Regards\nThe Team',)
        except:
            messages.error(request, "Problem Sending Email. Make sure your email is correct. If error persist contact a admin.")
            user.delete()
            return False
        rower.save()
        return True
    except IntegrityError as e:
        if "auth_user_username_key" in str(e):
            messages.error(request, "User allready exists")
        else:
            messages.error(request, "Unknown Error " + str(e))
        if user is not None:
            user.delete()
        return False

def construct_Outing(request, form):
    outing = None
    try:
        outing = Event(
            starting_time = form.cleaned_data['starting_time'],
            ending_time = form.cleaned_data['ending_time'],
            boat = form.cleaned_data['boat'],
            crew = form.cleaned_data['crew'],
            oars = form.cleaned_data['blades'],
            coxBox = form.cleaned_data['coxBox'],
            isRace = form.cleaned_data['isRace'],
            is_confirmed = form.cleaned_data['is_confirmed']
        )
        print("Senidng Email")
        try:
            rowers = outing.crew.members.all()
            emails = []
            for rower in rowers:
                emails.append(rower.user.email)
            send_mail('[Rowing Organizer]New Outing created for ' + outing.crew.name,
                      'Hello, \nA new outing was created for crew ' + outing.crew.name + '\n'+\
                      'Start Time: ' + str(outing.starting_time) + '\n'+\
                      'End Time:   '+ str(outing.ending_time) + '\n'+ \
                      'Boat:       ' + str(outing.boat.name) + '\n\n' +\
                      'Go to the website, if you want to Row in this outing.',
                      'no-reply@rowing.org',
                      emails,
                      fail_silently=False)
        except:
            messages.error(request, "Could not send email to all crew members. Outing was saved no the less.")
        outing.save()
        print("Created Outing")
        return True
    except IntegrityError as e:

        messages.error(request, "Unknown Error " + str(e))
        if outing is not None:
            outing.delete()
        return False

