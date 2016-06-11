from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from datetime import datetime
import logging
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Avg, F, Q, Value, Max
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Create your models here.

@python_2_unicode_compatible
class Pays(models.Model):
    nom = models.CharField(max_length=200)
    icone = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Tag(models.Model):
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    sort_id = models.IntegerField(default = 0)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Rencontre(models.Model):
    pays1 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p1_id') 
    pays2 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p2_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date = models.DateTimeField()
    comment = models.CharField(max_length=200, null=True, blank=True)
    allowNull = models.BooleanField(default=True)
    
    def passed(self):
        return self.date <= timezone.now()
    def __str__(self):
        return self.pays1.nom + ' - ' + self.pays2.nom + '('+self.date.isoformat()+')'

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField( null=True, blank=True, default= None)

    def score(self):
        if self.sc and self.nb:
            return self.sc/self.nb
        return 0
    def __str__(self):
        return self.name
    
        

class Member(models.Model):
    user = models.OneToOneField(User)
    team = models.ForeignKey(Team, null=True, blank=True, default = None)
    points = models.IntegerField(default=0)
    avatar = models.FileField(upload_to='euro/avatars', null=True, blank=True, default= None)
    def __str__(self):
        return self.user.username

@python_2_unicode_compatible    
class Pronostic(models.Model):
    member = models.ForeignKey(Member, on_delete= models.CASCADE)
    match = models.ForeignKey(Rencontre, on_delete = models.CASCADE)
    score1 = models.IntegerField(default=-1)
    score2 = models.IntegerField(default=-1)
    winner = models.IntegerField(default=-1)
    points = models.IntegerField(default=0)
    def __str__(self):
        return '[' + self.member.user.username + '] ' +  self.match.pays1.nom + ' - ' + self.match.pays2.nom + ' (' + str(self.score1) + ', ' + str(self.score2) + ')' + str(self.winner)

@python_2_unicode_compatible
class Resultat(models.Model):
    match = models.OneToOneField(Rencontre)
    score1 = models.IntegerField(default=-1)
    score2 = models.IntegerField(default=-1)
    winner = models.IntegerField(default=-1)
    def __str__(self):
        return self.match.pays1.nom + ' - ' + self.match.pays2.nom + ' (' + str(self.score1) + ', ' + str(self.score2) + ')'

# Model definissant une question True pour les QCM et False pour choix unique
@python_2_unicode_compatible
class MatchPool(models.Model):
    """
        Les sondages sont lies seulement a un match
        question : Il s'agit de la question qui est posee de mamniere generale
        reward : Le nombre de points accordes a ceux qui ont la bonne reponse
        leverage : Le levier demande par l'utilisateur
        multipleChoice : indique si une questione est un QCM ou non
    """
    match = models.ForeignKey(Rencontre)
    question = models.CharField(max_length=200, null=True, blank=True)
    reward = models.IntegerField(default=0)
    leverage = models.IntegerField(default=-1)
    enddate = models.DateField()
    multipleChoice = models.BooleanField(default=True)
    def __str__(self):
        return self.question + '  ' + self.match.__str__()

@python_2_unicode_compatible
class PollChoices(models.Model):
    poll =  models.ForeignKey(MatchPool)
    possibleResponseText = models.CharField(max_length=200, null=True, blank=True)
    possibleResponseNumber = models.IntegerField(default=-1)

    def __str__(self):
        return self.possibleResponseText


def my_callback(sender, instance, **kwargs):
    pronostics = Pronostic.objects.filter(match__exact=instance.match).all()
    for pronostic in pronostics :
        pronostic.points = 0
        if pronostic.score1 == instance.score1:
            pronostic.points += 1
        if pronostic.score2 == instance.score2:
            pronostic.points += 1
        if pronostic.score1 - pronostic.score2 == instance.score1 - instance.score2:
            pronostic.points += 2    
        if pronostic.winner == instance.winner:
            pronostic.points += 1
        pronostic.save()    
               

def handle_user_save(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)        
    
    
    
logger = logging.getLogger(__name__)    
post_save.connect(my_callback, sender=Resultat, dispatch_uid='update_resultat')
post_save.connect(handle_user_save, sender=User, dispatch_uid='update_user')

    
#class AvatarMember(models.Model):
#    user = models.OneToOneField(Member)
#    avatar = models.ImageField(upload_to='/images/')