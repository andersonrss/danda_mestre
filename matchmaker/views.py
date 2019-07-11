from django.shortcuts import render, render_to_response

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

#from django.core.urlresolvers import reverse
from django.urls import reverse

from django.contrib.auth.models import User

import random, os

# from matchmaker.models import MatchRF, MatchFF, MatchRFull

from .forms import LoginForm, ChangePasswordForm, AddMusicianForm

from .models import Musician

from matchmaker import utils

# Create your views here.


@login_required(login_url='/contest/login/')
def index_render(request):

    return HttpResponseRedirect( reverse('index') )

    if not utils.has_level_defined(request.user):
        return HttpResponseRedirect('/contest/levelchoose/')

    if not utils.has_matches_assigned(request.user):
        utils.assign_matches(request.user)

    if utils.has_unvoted_matches(request.user):
        contest = utils.get_contest(request.user)
    else: 
        return HttpResponseRedirect( reverse('thanks') )

    pages = ['main.html','reversemain.html']
    page = pages[random.randint(0,1)]

    # remaining_count = (9 - utils.get_count_contests_remaining(request.user)) +1
    remaining_count = (6 - utils.get_count_contests_remaining(request.user)) +1

    # return render( request, page, {'soloone': solo_one, 'solotwo': solo_two} )
    return render( request, page, {'contest': contest, 'remaining_count': remaining_count } )



@login_required(login_url='/contest/login/')
def single_evaluate_index_render(request):

    if not utils.has_level_defined(request.user):
        return HttpResponseRedirect('/contest/levelchoose/')

    if not utils.has_evaluations_assigned(request.user):
        utils.assign_evaluations(request.user)

    if utils.has_unevaluated_solos(request.user):
        solo = utils.get_evaluation(request.user)
    else: 
        return HttpResponseRedirect( reverse('thanks') )

    remaining_count = (6 - utils.get_count_evaluations_remaining(request.user)) +1

    if request.user.musician.firstaccess:
        return render(request, 'about.html',{})
    else:
        return render( request, 'evaluationmain.html', {'solo': solo, 'remaining_count': remaining_count } )



def login_view(request, login_error=False, passwordchanged=False):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect( reverse('index') )
            else:
                messages.error(request, 'Account not available.')
                return HttpResponseRedirect('/contest/login_error/')
        else:
            messages.error(request, 'Username or Password incorrect or account not available.')
            return HttpResponseRedirect('/contest/login_error/')
    else:
        form = LoginForm()
        form['username'].label_tag(attrs={'class': 'col-sm-2 control-label'})
        form['password'].label_tag(attrs={'class': 'col-sm-2 control-label'})
    
    return render(request, 'login.html', {'form': form, 'login_error': login_error,'passwordchanged': passwordchanged })



@login_required
def mark_firstaccess(request):
    if request.is_ajax() and request.method == 'POST':
        request.user.musician.firstaccess = False
        request.user.musician.save()
        return HttpResponse()
    else:
        return HttpResponseServerError()


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect( reverse('index') )



@login_required
def ajax_vote(request):

    if request.method == 'GET' :
        return HttpResponseForbidden('Yeah, Forbidden')


    if request.is_ajax():
        match = utils.vote_match( request.POST.get('matchtype'), int(request.POST.get('winner')), int(request.POST.get('usewinner')) )
        if match:
            return HttpResponse()
        else: 
            return HttpResponseServerError('Something wrong! Try Again, please.')
    else:
        return HttpResponseForbidden('Yeah, Forbidden')



@login_required(login_url='/contest/login/')
def changepassword(request):
    if request.method == 'POST':
        # print request.user.get_username()
        user = authenticate(
            username=request.user.get_username(),
            password=request.POST['old_password']
        )

        if user is not None:
            if user.is_active:
                new_password = request.POST['password']
                confirm_password = request.POST['confirm_password']

                if (new_password and new_password.strip()) and (confirm_password and confirm_password.strip()) and (new_password == confirm_password):
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return HttpResponseRedirect('/contest/passwordchanged/')
                else:
                    return HttpResponseRedirect('/contest/user/changepassword/?change=error')
            else:
                return HttpResponseRedirect('/contest/user/changepassword/?change=error')
        else:
            return HttpResponseRedirect('/contest/user/changepassword/?change=error')
    else:
        if request.GET.has_key('change') and request.GET.get('change') == 'error':
            change_error = True
        else:
            change_error = False
        form = ChangePasswordForm(initial={'username': request.user.get_username()})
        return render(request, 'changepassword.html', {'form': form, 'change_error': change_error})



@login_required
def addmlevel(request):
    if request.is_ajax():
        u = User.objects.get(pk=request.user.id)
        if request.POST.get('level'):
            lvl = request.POST.get('level')
            if lvl in ['b', 'B']:
                u.musician.level = Musician.BEGINNER
            elif lvl in ['i', 'I']:
                u.musician.level = Musician.INTERMEDIATE
            elif lvl in ['p', 'P']:
                u.musician.level = Musician.PROFESSIONAL
            u.musician.save()
            u.save()
        else:
            return HttpResponseServerError()
    else:
        return HttpResponseServerError()
    return HttpResponse()
    # return HttpResponseRedirect( reverse('index') )



@login_required
def add_musician(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('User is not staff')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not (password and password.strip()) or (password != confirm_password):
            return HttpResponseRedirect('/contest/addmusician/?addpass=error')
        else:
            user = User.objects.create_user(username, password=password)
            user.save()
            musician = Musician.create(user)
            musician.save()
            return HttpResponseRedirect('/contest/addmusician/?addmus=success')
    else:
        form  = AddMusicianForm()
        if request.GET.has_key('addpass') and request.GET.get('addpass') == 'error':
            addpasserror = True
        else: addpasserror = False

        if request.GET.has_key('addmus') and request.GET.get('addmus') == 'success':
            addmus = True
        else: addmus = False

        return render(request, 'addmusician.html', {'form': form, 'addpasserror': addpasserror, 'addmus': addmus})



@login_required
def solo_evaluation(request):
    if request.method == 'POST':
        utils.evaluate_solo( int(request.POST.get('evaluationtype')), int(request.POST.get('evaluationid')), 
            int(request.POST.get('solo-rate')), int(request.POST.get('usesolo')) )
        return HttpResponseRedirect( reverse('index') )
    else:
        return HttpResponseForbidden('Bad request')