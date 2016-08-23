from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import Group, User



from .models import Rower
from .forms import UserForm, OutingForm
from .user import construct_rower
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
            construct_rower(request, form)
            messages.success(request, "Your user hase been created. Please Wait for an Administror to accept your account.")
            return redirect('organizer/login')
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
    if request.POST:
        form = OutingForm(request.POST)
        if form.is_valid():
            messages.success(request, "The Outing has been created")
            response = redirect('organizer/main')
            return
        else:
            messages.error(request, form.non_field_errors())
    else:
        form = OutingForm()

    return render(request, 'organizer/create.html',
                  {'boatclub':{'name':'Champion on the Thames'},
                   'form':form,
                   'formname':"Outing",
                   'submit_name':"Create",
                   'post_url':"/organizer/createouting"})

@login_required(login_url='/organizer/login/')
def main(request):
    rower = get_object_or_404(Rower, pk=request.user)
    crews = rower.member_of_crew.all()

    return render(request, 'organizer/main.html', {
            'rower': rower,
            'crews': crews,
        })