from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from models import Pays, Rencontre, Member
from django.template import loader
from django.http import Http404
from django.views import generic
from django.core.urlresolvers import reverse
# Create your views here.


def index(request):
    latest_rencontre_list = Rencontre.objects.order_by('-date')[:5]
    
    context = {
        'latest_rencontre_list': latest_rencontre_list,
        'username' : request.session.get('username', None)
    }
    return render(request, 'euro/index.html', context)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def detail(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)




def login(request):
    m = Member.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        request.session['username'] = m.username
        return HttpResponseRedirect(reverse('euro:index'))
    else:
        return HttpResponse("Your username and password didn't match.")

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")    