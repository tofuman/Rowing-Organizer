from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.shortcuts import get_object_or_404, render, render_to_response, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Crew, Rower, Event
from .utils.enums import SIDE_CHOICES, GENDER_CHOICES
from .forms import UserForm
# Create your views here.

import logging

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/organizer/main/')
    return render_to_response('organizer/login.html', context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return render_to_response('organizer/login.html', context_instance=RequestContext(request))


def createuser(request):
    logout(request)
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            messages.info(request, "Your new User ("+ form.cleaned_data['username'] +") has been created! Please wait until a Administrator aproves the new user.")
    else:
        form = UserForm()

    return render(request, 'organizer/usercreation.html',
                  {'boatclub':{'name':'Champion on the Thames'},
                   'form':form})


@login_required(login_url='/organizer/login/')
def main(request):
    rower = get_object_or_404(Rower, pk=request.user)
    crews = rower.member_of_crew.all()

    return render(request, 'organizer/main.html', {
            'rower': rower,
            'crews': crews,
        })