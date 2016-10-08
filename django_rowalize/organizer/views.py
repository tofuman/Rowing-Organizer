from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext

from organizer.utils.constructObjects import construct_rower, construct_Outing
from .forms import UserForm, OutingForm
from .models import Rower, Crew, Event
from .utils.constans import RequestEmail
from .utils.helperMethods import createDefaultRenderArguments
from .rowingHelper.outing import modify

# Create your views here.



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
    templateargs = createDefaultRenderArguments(request)
    templateargs['form']= form
    return render(request, 'organizer/create.html',
                  templateargs)

@login_required(login_url='/organizer/login/')
def createouting(request):
    rower = Rower.objects.get(user=request.user)
    if request.POST:
        print("POST")
        form = OutingForm(request.POST)
        if form.is_valid():
            print("VALID")
            construct_Outing(request, form)
            messages.success(request, "The Outing has been created")
            return redirect('/organizer/main/')
        else:
            messages.error(request, form.non_field_errors())
    else:
        print("GET")
        if rower.organizes_crew.all():
            form = OutingForm()
        else:
            messages.warning(request, "No Crew to Organize!")
            return redirect('/organizer/main/')
    templateargs = createDefaultRenderArguments(request, rower)
    templateargs['form'] = form
    templateargs['formname']= "Outing"
    templateargs['submit_name'] = "Create"
    templateargs['post_url'] = "/organizer/createouting"
    templateargs['bar'] = True
    templateargs['requestemail'] = RequestEmail
    return render(request, 'organizer/create.html',
                  templateargs)

@login_required(login_url='/organizer/login/')
def changeOuting(request):


    messages.success(request, "Change to the Outing was successful.")
    return redirect('/organizer/main')

@login_required(login_url='/organizer/login/')
def outing(request, eventid=None):
    event = Event.objects.get(id=eventid)
    if event is None:
        messages.error(request, "Outing not Found!")
        return redirect('/organizer/main/')
    return modify(request, event)

@login_required(login_url='/organizer/login/')
def main(request, position='row'):
    rower = get_object_or_404(Rower, pk=request.user)
    if position == 'cox' and rower.is_cox:
        templateargs = createDefaultRenderArguments(request, rower)
        templateargs['coxed_crews'] = Crew.objects.all()
    elif position == 'coach' and rower.is_coach:
        templateargs = createDefaultRenderArguments(request, rower)
        templateargs['coach_crews'] = Crew.objects.all()
    elif position == 'org' and rower.organizes_crew.all():
        templateargs = createDefaultRenderArguments(request, rower)
        templateargs['organized_crews'] = rower.organizes_crew.all()
    else:
        templateargs = createDefaultRenderArguments(request, rower, rower.member_of_crew.all())

    templateargs['requestemail'] = RequestEmail
    return render(request, 'organizer/main.html', templateargs)
