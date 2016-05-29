from __future__ import unicode_literals

from django.db import models

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
    
class Rencontre(models.Model):
    pays1 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p1_id') 
    pays2 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p2_id')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.CharField(max_length=200)
    allowNull = models.BooleanField(default=True)
    def __str__(self):
        return self.pays1.nom + ' - ' + self.pays2.nom + '('+self.date.isoformat()+')'

class Member(models.Model):
    username = models.CharField(max_length=60)
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
    
    
#class AvatarMember(models.Model):
#    user = models.OneToOneField(Member)
#    avatar = models.ImageField(upload_to='/images/')