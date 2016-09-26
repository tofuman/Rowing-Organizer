from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import Group, User



from .models import Rower, Crew, Event
from .forms import UserForm, OutingForm
from .constructObjects import construct_rower, construct_Outing
# Create your views here.

import logging


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request,"User not found")
            return redirect('/organizer/login/')
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/organizer/main/')
            else:
                messages.warning(request,"The User is inactive.")
                return redirect('/organizer/login/')
        else:
            messages.warning(request,"Password not correct.")
            return redirect('/organizer/login/')
    return render_to_response('organizer/login.html', context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return render_to_response('organizer/login.html', context_instance=RequestContext(request))


def createuser(request):
    logout(request)
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            if construct_rower(request, form):
                messages.info(request, "Your new User (" + form.cleaned_data[
                    'username'] + ") has been created! Please wait until a Administrator aproves the new user.")
                return redirect('/organizer/login')
        else:
            messages.error(request, form.non_field_errors())
    else:
        form = UserForm()

    return render(request, 'organizer/create.html',
                  {'boatclub':{'name':'Champion on the Thames'},
                   'form':form,
                   'formname':"User",
                   'submit_name':"Register",
                   'post_url':"/organizer/createuser/"})

@login_required(login_url='/organizer/login/')
def createouting(request):
    rower = Rower.objects.get(user=request.user)
    if request.POST:
        form = OutingForm(request.POST)
        if form.is_valid():
            construct_Outing(request, form)
            messages.success(request, "The Outing has been created")
            return redirect('/organizer/main')
        else:
            messages.error(request, form.non_field_errors())
    else:
        if rower.organizes_crew.all():
            form = OutingForm()
        else:
            messages.warning(request, "No Crew to Organize!")
            return redirect('/organizer/main')
    return render(request, 'organizer/create.html',
                  {'boatclub':{'name':'Champion on the Thames'},
                   'form':form,
                   'rower':rower,
                   'formname':"Outing",
                   'submit_name':"Create",
                   'post_url':"/organizer/createouting/",
                   'bar': True})

@login_required(login_url='/organizer/login/')
def changeOuting(request):


    messages.success(request, "Change to the Outing was successful.")
    return redirect('/organizer/main')

@login_required(login_url='/organizer/login/')
def outing(request, eventid=None):
    action = request.GET.get('action')
    typ = request.GET.get('typ')
    event = Event.objects.get(id=eventid)
    rower = Rower.objects.get(user=request.user)
    if event is None:
        messages.error(request, "Outing not Found!")
        return redirect('/organizer/main/')

    if typ == 'row':
        if action == 'join':
            event.members.add(Rower.objects.get(user=request.user))
        elif action == 'leave' and event.members.filter(user=request.user).count() >0:
            event.members.remove(rower)
    if typ == 'cox' :
        if action == 'join'and event.cox is None:
            event.cox = (rower)
        elif action == 'leave' and event.cox is not None and event.cox == rower:
            print("OUT")
            event.cox = None
            rower.save()
    if typ == 'coach' :
        if action == 'join'and event.coaches is None:
            event.coaches = (rower)
        elif action == 'leave' and event.coaches is not None and event.coaches == rower:
            print("OUT")
            event.coaches = None
            rower.save()

    event.save()
    if action == 'join':
        messages.success(request, 'Joint Outing')
    elif action == 'leave':
        messages.error(request, 'Oped Out')
    return redirect('/organizer/main/')

@login_required(login_url='/organizer/login/')
def main(request):
    rower = get_object_or_404(Rower, pk=request.user)
    crews = rower.member_of_crew.all()
    coxed_crews = None
    coach_crews = None
    if rower.is_coach:
        coxed_crews = Crew.objects.all()
    if rower.is_cox:
        coach_crews = Crew.objects.all()
    return render(request, 'organizer/main.html', {
            'rower': rower,
            'crews': crews,
            'coxed_crews' : coxed_crews,
            'coach_crews': coach_crews,
            'organized_crews' : rower.organizes_crew.all(),
        })