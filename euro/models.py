from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Create your models here.
class Pays(models.Model):
    nom = models.CharField(max_length=200)
    icone = models.CharField(max_length=200)
    def __str__(self):
        return self.nom



class Rencontre(models.Model):
    pays1 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p1_id') 
    pays2 = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name = 'p2_id')
    date = models.DateField()
    comment = models.CharField(max_length=200)
    def __str__(self):
        return self.pays1.nom + ' - ' + self.pays2.nom + '('+self.date.isoformat()+')'

class Member(models.Model):
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    def __str__(self):
        return self.username    