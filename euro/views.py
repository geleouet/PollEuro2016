from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from models import Pays, Rencontre, Member, Pronostic, Tag
from django.template import loader
from django.http import Http404
from django.views import generic
from django.core.urlresolvers import reverse
from django.core import serializers
# Create your views here.


def index(request):
    latest_rencontre_list = Tag.objects.all()
    
    context = {
        'latest_rencontre_list': latest_rencontre_list,
        'username' : request.session.get('username', None)
    }
    return render(request, 'euro/index.html', context)


def next_matchs(request):
    latest_rencontre_list = Rencontre.objects.order_by('-date')[:5]
    latest_rencontre_date = set(map(lambda r: r.date ,latest_rencontre_list))
    context = {
        'latest_rencontre_list': latest_rencontre_list,
        'username' : request.session.get('username', None)
    }
    return render(request, 'euro/nexts.html', context)



def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def detail(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def register(request):
    newMember = Member()
    newMember.username = request.POST['username']
    newMember.password = request.POST['password']
    newMember.email = request.POST['email']
    newMember.save()
    request.session['member_id'] = newMember.id
    request.session['username'] = newMember.username
    return HttpResponseRedirect(reverse('euro:index'))

def check_login(request):
    try :
        m = Member.objects.get(username=request.POST['username'])
    except (KeyError, Member.DoesNotExist) :
            return JsonResponse({'reason' : 'User doesn\'t exists.'})
    else :
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            request.session['username'] = m.username
            return JsonResponse({'success' : '/success'})
        else:
            return JsonResponse({'reason' : 'Your username and password didn\'t match.'})


def login(request):
    try :
        m = Member.objects.get(username=request.POST['username'])
    except (KeyError, Member.DoesNotExist) :
        return HttpResponse("Your username and password didn't match.")
    else :
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            request.session['username'] = m.username
            return HttpResponseRedirect(reverse('euro:index'))
        else:
            return HttpResponse("Your username and password didn't match.")

def logout(request):
    try:
        del request.session['member_id']
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('euro:index'))
