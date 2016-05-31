from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.db import models
from datetime import datetime
import logging


# Create your models here.

# Create your models here.
class Pays(models.Model):
    nom = models.CharField(max_length=200)
    icone = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Tag(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    def matchs(self):
        return Rencontre.objects.filter(tag=self).order_by('date').all()
    
class Rencontre(models.Model):
    pays1 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p1_id') 
    pays2 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p2_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.CharField(max_length=200)
    allowNull = models.BooleanField(default=True)
    def passed(self):
        return self.date <= datetime.date(datetime.now())
    def __str__(self):
        return self.pays1.nom + ' - ' + self.pays2.nom + '('+self.date.isoformat()+')'

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Member(models.Model):
    username = models.CharField(max_length=60)
    team = models.ForeignKey(Team, null=True, blank=True, default = None)
    password = models.CharField(max_length=60)
    email = models.CharField(max_length=120)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Pronostic(models.Model):
    member = models.ForeignKey(Member, on_delete= models.CASCADE)
    match = models.ForeignKey(Rencontre, on_delete = models.CASCADE)
    score1 = models.IntegerField(default=-1)
    score2 = models.IntegerField(default=-1)
    winner = models.IntegerField(default=-1)
    points = models.IntegerField(default=-1)
    def __str__(self):
        return '[' + self.member.username + '] ' +  self.match.pays1.nom + ' - ' + self.match.pays2.nom + ' (' + str(self.score1) + ', ' + str(self.score2) + ')'
    
class Resultat(models.Model):
    match = models.ForeignKey(Rencontre, on_delete = models.CASCADE)
    score1 = models.IntegerField(default=-1)
    score2 = models.IntegerField(default=-1)
    winner = models.IntegerField(default=-1)
    def __str__(self):
        return self.match.pays1.nom + ' - ' + self.match.pays2.nom + ' (' + str(self.score1) + ', ' + str(self.score2) + ')'


def my_callback(sender, instance, **kwargs):
    print(str(instance) + " finished!")
    pronostics = Pronostic.objects.filter(match__exact=instance.match).all()
    for pronostic in pronostics :
        pronostic.points = 0
        if pronostic.score1 == instance.score1:
            pronostic.points += 1
        if pronostic.score2 == instance.score2:
            pronostic.points += 1
        if pronostic.winner == instance.winner:
            pronostic.points += 1
        pronostic.save()    
               
        
    
    
    
logger = logging.getLogger(__name__)    
post_save.connect(my_callback, sender=Resultat, dispatch_uid='update_resultat')
    
    
#class AvatarMember(models.Model):
#    user = models.OneToOneField(Member)
#    avatar = models.ImageField(upload_to='/images/')