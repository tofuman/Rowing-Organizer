from django import forms
from .utils.enums import GENDER_CHOICES, SIDE_CHOICES

class UserForm(forms.Form):
    username = forms.CharField(label='Pick a username', max_length=100)
    name = forms.CharField(label='Your name', max_length=40)
    password = forms.PasswordInput()
    retypedpassword = forms.PasswordInput()
    email = forms.EmailField(label='Your Email')
    phone_number = forms.CharField(max_length=20)  # TODO !!!
    preferred_side = forms.ChoiceField(required=True, choices=SIDE_CHOICES)
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)
    is_cox = forms.BooleanField( required=False)
    is_coach = forms.BooleanField(required=False)