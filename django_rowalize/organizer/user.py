from .models import User,Rower
from django.db.utils import IntegrityError
from django.contrib import messages


def construct_rower(request, form):
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
        rower.save()
        messages.info(request, "Your new User (" + form.cleaned_data[
            'username'] + ") has been created! Please wait until a Administrator aproves the new user.")
    except IntegrityError as e:
        if "auth_user_username_key" in str(e):
            messages.error(request, "User allready exists")
