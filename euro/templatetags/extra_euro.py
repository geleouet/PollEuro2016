from django import template
from euro.models import Pays, Rencontre, Member, Pronostic, Tag


register = template.Library()


def score1(value, arg):
    if (value.filter(match__exact=arg).exists()):
        try :
            return value.get(match__exact=arg).score1
        except (KeyError, Pronostic.DoesNotExist, RelatedObjectDoesNotExist ) :
            return -1
    else:   
        return None

def score2(value, arg):
    if (value.filter(match__exact=arg).exists()):
        try :
            return value.get(match__exact=arg).score2
        except (KeyError, Pronostic.DoesNotExist, RelatedObjectDoesNotExist ) :
            return -1
    else:   
        return None
    
register.filter('score1', score1)
register.filter('score2', score2)