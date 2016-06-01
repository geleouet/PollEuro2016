from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Count, Min, Sum, Avg, F, Q, Value, Max
from models import Pays, Rencontre, Member, Pronostic, Tag, Resultat,  Team
from django.template import loader
from django.http import Http404
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import serializers
from datetime import datetime
from django.shortcuts import redirect
#from .forms import memberUpdateForm
from django.contrib.auth import authenticate, login, logout
import logging

# Create your views here.


def home(request):
    if request.user.is_authenticated() == False:
        return index(request)
   
    user =request.user.member
    latest_rencontre_list = Rencontre.objects.filter(date__gte=datetime.now()).order_by('-date')[:5]
    latest_rencontre_date = sorted(set(map(lambda r: r.date ,latest_rencontre_list)))
    pron = Pronostic.objects.filter(member__exact = user)
    pronostics = pron.all()
    user.pts = pron.exclude(points__exact=-1).aggregate(pts=Sum('points'))['pts'] 
    
    latest_pronostics = pron.filter(match__date__gte=datetime.now()).order_by('-match__date')[:5]
    resultats = Resultat.objects.filter(match__in=pron.values_list('match', flat=True)).all()
    for res in resultats :
        res.points = pronostics.filter(match__exact=res.match).get().points
    print resultats
    
    
    context = {
        'user': user,
        'username' : request.session.get('username', None),
        'latest_rencontre_list' : latest_rencontre_list,
        'latest_rencontre_date': latest_rencontre_date,
        'pronostics':pronostics,
        'latest_pronostics':latest_pronostics,
        'resultats':resultats,
        #'temp':temp,
    }
    
    
    return render(request, 'euro/home.html', context)

def classement(request):
    if request.user.is_authenticated():
        user = request.user.member
    else:
        user = None
        self_user = None
     
    users = Member.objects.annotate(score=Sum('pronostic__points')).order_by('-score').all()
    
    context = {
        'users': users,
        'self': user,
        'username' : request.session.get('username', None),
        
    }
    return render(request, 'euro/classement.html', context)
    

def index(request):
    
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None
        
    tag_list = Tag.objects.filter(enabled__exact=True).select_related().annotate(maxDate=Max('rencontre__date')).all()   
    
    pronostics = Pronostic.objects.filter(member__exact = user).all()
    context = {
        'tag_list': tag_list,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
    }
    return render(request, 'euro/index.html', context)


def next_matchs(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None
    
    latest_rencontre_list = Rencontre.objects.filter(date__gte=datetime.now()).order_by('-date')[:15]
    latest_rencontre_date = sorted(set(map(lambda r: r.date ,latest_rencontre_list)))
    pronostics = Pronostic.objects.filter(member__exact = user).all()
    context = {
        'latest_rencontre_list': latest_rencontre_list,
        'latest_rencontre_date': latest_rencontre_date,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
    }
    return render(request, 'euro/nexts.html', context)


def register(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    request.session['member_id'] = user.id
    request.session['username'] = user.username
    return HttpResponseRedirect(reverse('euro:index'))

def check_login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            request.session['member_id'] = user.id
            request.session['username'] = user.username
            return JsonResponse({'success' : '/success'})            
        else:
            return JsonResponse({'reason' : 'Account has been deactivated.'})
    else:
        # the authentication system was unable to verify the username and password
        return JsonResponse({'reason' : 'Your username and password didn\'t match.'})


def save(request):
    if request.user.is_authenticated():
        user =request.user.member
        score1 = {}
        score2 = {}
        winner = {}
        res =''
        for item in request.POST.items():
            res += 'item '+ str(item) +' :'
            if (item[0].find('score')>-1 and item[1] != '' and item[0].find('radio') == -1):
                match = item[0].split('_')[1]
                score = item[1]
                if (int(item[0].split('_')[2]) == 1):
                    score1[match] = score
                else:
                    score2[match] = score
            elif (item[0].find('score')>-1 and item[1] != '' and item[0].find('radio') > -1):
                match = item[0].split('_')[1]
                winner[match] = item[1]     
        
        for item in score1.items():
            if (score2[item[0]]):
                rencontre = Rencontre.objects.get(pk=item[0])
                p, created = Pronostic.objects.filter(match__exact=item[0]).filter(member__exact=user).get_or_create(
                    member=user,
                    match=rencontre
                )
                p.score1 = score1[item[0]]
                p.score2 = score2[item[0]]
                if score1[item[0]] == score2[item[0]] :
                    p.winner = winner[item[0]]
                else :   
                    p.winner = 1 if score1[item[0]] > score2[item[0]] else 2
                print str(p)
                p.save()
                    
        return JsonResponse({'success' : 'success', 'res' : res})        
        
    else :
        return JsonResponse({'reason' : 'User doesn\'t exists.', 'pk' : request.session['member_id']})
    

def manageteam(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None

    pronostics = Pronostic.objects.filter(member__exact = user).all()
    listOfTeams = Team.objects.all()
    userform = memberUpdateForm(request.POST or None)

    context = {
        'user': user,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
        'listOfTeams' : listOfTeams,
        'userform' : userform
    }

    if request.method == 'POST':
        instance = userform.save(commit=True)
        instance.save()

    return render(request, 'euro/userteam.html', context)

def addUserToTeam(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None


    userform = memberUpdateForm(request.POST or None)

    if userform.is_valid():
            userform.save()

    context = {
        'user': user,
        'username' : request.session.get('username', None),
        'userform' : userform,
    }
    return render(request, 'euro/userTeamChanged.html', context)



def logout_view(request):
    try:
        logout(request)
        del request.session['member_id']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('euro:index'))
