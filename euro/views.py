from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg, F, Q, Value, Max
from models import Pays, Rencontre, Member, Pronostic, Tag, Resultat,  Team, PollChoices, MatchPool
from django.template import loader
from django.http import Http404
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import serializers
from datetime import datetime

from django.shortcuts import redirect
from .forms import memberUpdateForm, creatTeam
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.files.base import File
import logging
from django.core.mail import send_mail
from datetime import timedelta
from django.core.signing import Signer, BadSignature
from urllib import quote, unquote
from  django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def changeResestPassword(request):
    token = request.POST['token']
    if token:
        signer = Signer()
        try:
            original = signer.unsign(token)
        except BadSignature:
            print("Tampering detected!")
            return JsonResponse({'error' : 'token expired'})
        
        user = User.objects.filter(username=original).get()
        newPass = request.POST['password']
        user.password = make_password(newPass)
        user.save()
        user = authenticate(username=original, password=newPass)
        login(request, user)
        request.session['member_id'] = user.id
        request.session['username'] = user.username
        return JsonResponse({'success' : 'password changed for ' + user.username})
    else:
        if request.user.is_authenticated():
            me = request.user
            if check_password(request.POST['password0'], me.password):
                newPass = request.POST['password']
                me.password = make_password(newPass)
                me.save()
                me = authenticate(username=me.username, password=newPass)
                login(request, me)
                return JsonResponse({'success' : 'password changed for ' + me.username})
            else:
                return JsonResponse({'error' : 'current password doesn\'t match'})
            
    return JsonResponse({'error' : 'password not changed'})

def changeEmail(request):
    if request.user.is_authenticated():
        me = request.user
        me.email=request.POST['email']
        me.save()
        
        return JsonResponse({'success' : 'email changed for ' + me.username + '->' + request.POST['email']})
    return JsonResponse({'error' : 'user not authenticated'})

def changePassword(request):
    if request.user.is_authenticated():
        me = request.user
        signer = Signer()
        value = signer.sign(me.username)
        context = {
            'user': me,
            'token': value,
            'self': me.member,
            'username' : request.session.get('username', None),
        }
        return render(request, 'euro/resetPassword.html', context)
   
    return HttpResponseRedirect(reverse('euro:index'))

def resetPassword(request):
    token = request.GET['token']
    if token:
        signer = Signer()
        try:
            original = signer.unsign(token)
        except BadSignature:
            print("Tampering detected!")
            return HttpResponseRedirect(reverse('euro:index'))
        print 'reset password for ' + original    
        user = User.objects.filter(username=original).get()
        context = {
            'user': user,
            'token': token,
        }
        return render(request, 'euro/resetPassword.html', context)
   
    return HttpResponseRedirect(reverse('euro:index'))
    

def reset(request):
    try:
        membre = request.POST['username']
        mail = User.objects.filter(username=membre).get().email
        if mail != request.POST['email']:
            return JsonResponse({'error' : 'user name and email doesn\'t correspond'})
        signer = Signer()
        value = signer.sign(membre)
        link = settings.ABSOLUTE_URL + reverse("euro:resetPassword") + "?token=" + quote(value)
        msg = 'Hi ' + membre +'\n'
        msg +='You recently asked to change your password\n'
        msg +='click on the following link to proceed:\n'
        msg +=link
        msg +='\n'
        send_mail('[Pronostic-euro206] Password change request', msg, 'contact@pronostic-euro2016.eu', [mail], fail_silently=False)
    
        return JsonResponse({'success' : ('email sent to ' + mail + ";" + link)})
        
    except ObjectDoesNotExist:
        return JsonResponse({'error' : 'invalid user name'})


def mail(request):
    send_mail('Sujet test', 'message test', 'contact@pronostic-euro2016.eu', ['gaetan.eleouet@gmail.com'], fail_silently=False)
    return HttpResponseRedirect(reverse('euro:index'))

def view_member(request, mid):
    if request.user.is_authenticated():
        me = request.user.member
    else:
        me = None

    user = Member.objects.filter(id=mid).get()
    latest_rencontre_list = Rencontre.objects.filter(date__gte=datetime.now()).select_related().order_by('date')[:5]
    latest_rencontre_date = sorted(set(map(lambda r: r.date.date() ,latest_rencontre_list)))
    
    pronostics_set = Pronostic.objects.filter(member__exact = user).select_related('match').all()
    pronostics = {x.match: x for x in pronostics_set}
    
    user.pts = pronostics_set.aggregate(pts=Sum('points'))['pts']

    latest_pronostics = pronostics_set.filter(match__date__gte=datetime.now()).order_by('-match__date')[:5]
    
    resultats_set = Resultat.objects.filter(match__in=pronostics_set.values_list('match', flat=True)).select_related('match__pays1').select_related('match__pays2').all()
    for res in resultats_set :
        res.points = pronostics[res.match].points
        
    resultats = {r.match : r for r in resultats_set}


    context = {
        'user': user,
        'self':me,
        'edit': user == me,
        'username' : request.session.get('username', None),
        'latest_rencontre_list' : latest_rencontre_list,
        'latest_rencontre_date': latest_rencontre_date,
        'resultats_set': resultats_set,
        'pronostics':pronostics,
        'latest_pronostics':latest_pronostics,
        'resultats':resultats,
        #'temp':temp,
    }


    return render(request, 'euro/home.html', context)

def faq(request):
    if request.user.is_authenticated():
        user = request.user.member
    else:
        user = None
        self_user = None

    context = {
        'self': user,
        'username' : request.session.get('username', None),

    }
    return render(request, 'euro/faq.html', context)


def home(request):
    if request.user.is_authenticated() == False:
        return index(request)

    user =request.user.member
    latest_rencontre_list = Rencontre.objects.filter(date__gte=datetime.now()).select_related().order_by('date')[:5]
    latest_rencontre_date = sorted(set(map(lambda r: r.date.date() ,latest_rencontre_list)))
    
    pronostics_set = Pronostic.objects.filter(member__exact = user).select_related('match').all()
    pronostics = {x.match: x for x in pronostics_set}
    
    user.pts = pronostics_set.aggregate(pts=Sum('points'))['pts']

    latest_pronostics = pronostics_set.filter(match__date__gte=datetime.now()).order_by('-match__date')[:5]
    
    resultats_set = Resultat.objects.filter(match__in=pronostics_set.values_list('match', flat=True)).select_related('match__pays1').select_related('match__pays2').all()
    for res in resultats_set :
        res.points = pronostics[res.match].points
        
    resultats = {r.match : r for r in resultats_set}

    context = {
        'user': user,
        'self': user,
        'edit':True,
        'username' : request.session.get('username', None),
        'latest_rencontre_list' : latest_rencontre_list,
        'latest_rencontre_date': latest_rencontre_date,
        'resultats_set': resultats_set,
        'pronostics':pronostics,
        'latest_pronostics':latest_pronostics,
        'resultats':resultats,
        'allTeams':Team.objects.order_by('name'),
        #'temp':temp,
    }


    return render(request, 'euro/home.html', context)

def classement(request):
    if request.user.is_authenticated():
        user = request.user.member
    else:
        user = None
        self_user = None

    users = Member.objects.annotate(score=Sum('pronostic__points')).annotate(nb=Count('pronostic')).select_related('user').select_related('team').order_by( (0 * F('score'))).order_by('score').all()
    
    context = {
        'users': users,
        'self': user,
        'username' : request.session.get('username', None),

    }
    return render(request, 'euro/classement.html', context)


def team(request, mid):
    if request.user.is_authenticated():
        user = request.user.member
    else:
        user = None
        self_user = None

    users = Member.objects.filter(team_id=mid).select_related('user').annotate(score=Sum('pronostic__points')).order_by('-score').all()

    context = {
        'users': users,
        'self': user,
        'username' : request.session.get('username', None),
        'team': Team.objects.filter(id=mid).annotate(sc=Sum('member__pronostic__points')).get(),

    }
    return render(request, 'euro/classement.html', context)

def classement_teams(request):
    if request.user.is_authenticated():
        user = request.user.member
    else:
        user = None
        self_user = None

    teams = Team.objects.prefetch_related('member_set__pronostic_set').annotate(sc=Avg('member__pronostic__points')).order_by('-sc').all()
    
    context = {
        'teams': teams,
        'self': user,
        'username' : request.session.get('username', None),
    }
    return render(request, 'euro/classement_teams.html', context)


def change_team(request):
    if request.user.is_authenticated():
        user = request.user.member
        if str(request.POST['id_team']) == 'None':
            if request.POST.get('new_team', None):
                team = Team.objects.create(name=str(request.POST['new_team']), description='')
                user.team = team
            else:
                user.team = None
        else :
            user.team = Team.objects.filter(id=request.POST['id_team']).get()
        user.save()
        return JsonResponse({'success' : '/success'})
    else:
         return JsonResponse({'reason' : 'You are not authenticated.'})


def upload(request):
    # Handle file upload
    if request.user.is_authenticated():
         user = request.user.member
         if request.method == 'POST':
            img_data = request.POST['image-data'].split(',')[1].decode("base64")
            name = user.user.username + datetime.now().strftime('%Y%m%d') +".jpg"
            path = settings.MEDIA_ROOT + name
            img_file = open(path, "wb")
            img_file.write(img_data)
            img_file.close()

            user = request.user.member
            user.avatar.name = name
            user.save();

            return JsonResponse({'success' : '/success'})
         else:
            return JsonResponse({'reason' : 'invalid request'})
    else:
         return JsonResponse({'reason' : 'you are not logged in'})




def change_desc(request, mid):
    if request.user.is_authenticated():
        user = request.user.member
        if str(user.team.id) == str(mid):
            user.team.description = request.POST['description']
            user.team.save()
            return JsonResponse({'success' : '/success'})
        else:
            return JsonResponse({'reason' : 'this is not your team'})
    else:
         return JsonResponse({'reason' : 'You are not authenticated.'})



def index(request):

    if request.user.is_authenticated():
        user = request.user.member
    else:
        user = None

    tag_list = Tag.objects.filter(enabled__exact=True).prefetch_related('rencontre_set__resultat').prefetch_related('rencontre_set__pays1').prefetch_related('rencontre_set__pays2').annotate(maxDate=Max('rencontre__date')).order_by('sort_id').all()

    pronostics_set = Pronostic.objects.filter(member__exact = user).select_related('match').all()
    pronostics = {x.match: x for x in pronostics_set}
    context = {
        'tag_list': tag_list,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
        'self':user,
    }
    return render(request, 'euro/index.html', context)


def next_matchs(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None

    latest_rencontre_list = Rencontre.objects.filter(date__gte=datetime.now()).select_related('pays1').select_related('pays2').order_by('date')
    latest_rencontre_date = sorted(set(map(lambda r: r.date.date() ,latest_rencontre_list)))  
    pronostics_set = Pronostic.objects.filter(member__exact = user).select_related('match').all()
    pronostics = {x.match: x for x in pronostics_set}
    context = {
        'latest_rencontre_list': latest_rencontre_list,
        'latest_rencontre_date': latest_rencontre_date,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
        'self':user,
    }
    return render(request, 'euro/nexts.html', context)


def register(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    request.session['member_id'] = user.id
    request.session['username'] = user.username
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    login(request, user)
    return HttpResponseRedirect(reverse('euro:home'))

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
                if rencontre.passed():
                    pass
                else:    
                    try :
                        if rencontre.resultat:
                            continue
                        if rencontre.passed:
                            continue
                    except (KeyError, ObjectDoesNotExist) :
                        pass

                    p, created = Pronostic.objects.filter(match__exact=item[0]).filter(member__exact=user).get_or_create(
                        member=user,
                        match=rencontre
                    )
                    p.score1 = score1[item[0]]
                    p.score2 = score2[item[0]]
                    if score1[item[0]] == score2[item[0]] and item[0] in winner :
                        p.winner = winner[item[0]]
                    elif score1[item[0]] == score2[item[0]]:
                        p.winner = -1
                    else :
                        p.winner = 1 if score1[item[0]] > score2[item[0]] else 2
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
    TeamFrom = creatTeam()

    context = {
        'user': user,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
        'listOfTeams' : listOfTeams,
        'userform' : userform,
        'TeamFrom' : TeamFrom
    }

    if request.method == 'POST':
        instance = userform
        instance.save(request)

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


def landinPage(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None

    latest_rencontre_list = Rencontre.objects.filter(date__gte=datetime.now()).select_related('pays1').select_related('pays2').order_by('date')
    latest_rencontre_date = sorted(set(map(lambda r: r.date.date() ,latest_rencontre_list)))  
    pronostics_set = Pronostic.objects.filter(member__exact = user).select_related('match').all()
    pronostics = {x.match: x for x in pronostics_set}
    
    context = {
        'latest_rencontre_list': latest_rencontre_list,
        'latest_rencontre_date': latest_rencontre_date,
        'username' : request.session.get('username', None),
        'pronostics':pronostics,
    }
    return render(request, 'euro/landingpage.html', context)

# About Us page

def aboutus(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None
    context = {
        'self': user,
        'username' : request.session.get('username', None),
    }
    return render(request, 'euro/aboutus.html', context)

def displaypolls(request):
    if request.user.is_authenticated():
        user =request.user.member
    else:
        user = None

    questionnaire_list = MatchPool.objects.all()

    choices = PollChoices.objects.all()

    context = {
        'questionnaire_list': questionnaire_list,
        'choices': choices,
    }

    return render(request, 'euro/questionderives.html', context)

def logout_view(request):
    try:
        logout(request)
        del request.session['member_id']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('euro:index'))
