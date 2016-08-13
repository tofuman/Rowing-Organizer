from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.shortcuts import get_object_or_404, render, render_to_response, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


from .models import Crew, Rower, Event
from .utils.enums import SIDE_CHOICES, GENDER_CHOICES
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
    return render(request, 'organizer/usercreation.html',
                  {'boatclub':{'name':'Champion on the Thames'},
                   'sides':SIDE_CHOICES,
                   'genders': GENDER_CHOICES})


@login_required(login_url='/organizer/login/')
def main(request):
    rower = get_object_or_404(Rower, pk=request.user)
    crews = rower.member_of_crew.all()

    return render(request, 'organizer/main.html', {
            'rower': rower,
            'crews': crews,
        })