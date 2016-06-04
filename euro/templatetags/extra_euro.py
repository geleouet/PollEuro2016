from django import template
from euro.models import Pays, Rencontre, Member, Pronostic, Tag
from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls.static import static
from django.conf import settings

register = template.Library()


def score1(value, arg):
    try :
        return value.get(match__exact=arg).score1
    except (KeyError, ObjectDoesNotExist) :
        return None


def score2(value, arg):
    try :
        return value.get(match__exact=arg).score2
    except (KeyError, ObjectDoesNotExist) :
        return None

def points(value, arg):
    try :
        return value.get(match__exact=arg).points
    except (KeyError, ObjectDoesNotExist) :
        return None
    
def winner(value, arg):
    try :
        return value.get(match__exact=arg).winner
    except (KeyError, ObjectDoesNotExist) :
        return None    
    
def avatar(value):
    if (value and value.avatar ):
        return settings.MEDIA_URL + value.avatar.name
    else:
        return settings.STATIC_URL + "euro/images/256.jpg"

    
@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )    
    
register.filter('score1', score1)
register.filter('score2', score2)
register.filter('points', points)
register.filter('winner', winner)
register.filter('avatar', avatar)