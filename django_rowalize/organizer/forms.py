from django import forms
from .utils.enums import GENDER_CHOICES, SIDE_CHOICES
from .models import Event, CoxBox
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from datetime import datetime
from django.utils.timezone import get_current_timezone

class UserForm(forms.Form):
    username = forms.CharField(label='Pick a username', max_length=100)
    first_name = forms.CharField(label='Your First name', max_length=40)
    sir_name = forms.CharField(label='Your Surname', max_length=40)
    password = forms.CharField(label='Please pick a secure password', widget=forms.PasswordInput(render_value=True))
    retyped_password = forms.CharField(label='Please confirm your password',widget=forms.PasswordInput(render_value=True))
    email = forms.EmailField(label='Your Email address')
    retype_email = forms.EmailField(label='Please confirm your Email address')
    phone_number = forms.CharField(label='Please give a contact phone number', max_length=20)  # TODO !!!
    preferred_side = forms.ChoiceField(label='Please select a preferred side', required=True, choices=SIDE_CHOICES)
    gender = forms.ChoiceField(label='Please specify your the gender you row with', required=True, choices=GENDER_CHOICES)
    is_cox = forms.BooleanField(label='I am happy cox', required=False)
    is_coach = forms.BooleanField(label='I am happy coach', required=False)

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
    dateTimeOptions = {
        'format': 'dd/mm/yy hh:ii',
        'autoclose': True,
        'minuteStep':'15',
        'weekStart':'1',
        'startDate' : str(datetime.now(get_current_timezone())),
        'todayHighlight':True,
        'pickerPosition':'bottom-left',
        }


    class Meta:
        model = Event
        fields = [
            'crew',
            'starting_time',
            'ending_time',
            'boat',
            'blades',
            'coxBox',
            'isRace',
            'is_confirmed'
        ]
    def __init__(self, *args, **kwargs):
        super(OutingForm, self).__init__(*args, **kwargs)
        self.fields['starting_time'] = forms.DateTimeField(widget=DateTimeWidget(usel10n=True,
                                                                                 bootstrap_version=3,
                                                                                 options=self.dateTimeOptions))
        self.fields['ending_time'] = forms.DateTimeField(widget=DateTimeWidget(usel10n=True,
                                                                               bootstrap_version=3,
                                                                               options=self.dateTimeOptions))
        self.fields['isRace'] = forms.BooleanField(label='This Outing is a Race', required=False)
        self.fields['is_confirmed'] = forms.BooleanField(label='This outing is already confirmed', required=False)
        self.fields['coxBox'].label = "Cox Box"
        self.fields['coxBox'].required = False

    def clean(self):
        self.cleaned_data = super(OutingForm, self).clean()
        try:
            starting_time = self.cleaned_data.get('starting_time')
            ending_time = self.cleaned_data.get('ending_time')
        except ValueError:
            raise forms.ValidationError("Time is Wrong!")
        except TypeError:
            print(self.cleaned_data.get('starting_time').split('+')[0])

            raise forms.ValidationError("Start or End time was left empty")
        if starting_time is None or ending_time is None:
            raise forms.ValidationError("Please give start and end times!")
        if datetime.now(get_current_timezone()) >= starting_time or datetime.now(get_current_timezone())  >= ending_time:
            raise forms.ValidationError("Time is in the past!")
        if starting_time > ending_time:
            raise forms.ValidationError("End Time is prior to Start Time!")

        return self.cleaned_data
