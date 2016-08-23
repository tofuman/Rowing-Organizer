from django import forms
from .utils.enums import GENDER_CHOICES, SIDE_CHOICES
from .models import Event

class UserForm(forms.Form):
    username = forms.CharField(label='Pick a username', max_length=100)
    first_name = forms.CharField(label='Your first name', max_length=40)
    sir_name = forms.CharField(label='Your Sir name', max_length=40)
    password = forms.CharField(label='please pick a secure password', widget=forms.PasswordInput(render_value=True))
    retyped_password = forms.CharField(label='Please confirm your password',widget=forms.PasswordInput(render_value=True))
    email = forms.EmailField(label='Your Email address')
    retype_email = forms.EmailField(label='Please confirm your Email address')
    phone_number = forms.CharField(label='Please give a contact phone number', max_length=20)  # TODO !!!
    preferred_side = forms.ChoiceField(label='Please selcet a prefered side', required=True, choices=SIDE_CHOICES)
    gender = forms.ChoiceField(label='Please sepcifvy your the gender you row with',required=True, choices=GENDER_CHOICES)
    is_cox = forms.BooleanField(label='I am a cox', required=False)
    is_coach = forms.BooleanField(label='I am a coach', required=False)

    def clean(self):
        self.cleaned_data = super(UserForm, self).clean()

        password = self.cleaned_data.get('password')
        retype = self.cleaned_data.get('retyped_password')
        if password and password != retype:
            raise forms.ValidationError("Passwords did not match!")

        email = self.cleaned_data.get('email')
        retype_email = self.cleaned_data.get('retype_email')
        if email and email != retype_email:
            raise forms.ValidationError("Email addresses dit not match!")

        return self.cleaned_data

class OutingForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'starting_time',
            'ending_time',
            'boat',
            'coaches',
            'crew',
            'members',
            'oars',
            'coxBox'
        ]
