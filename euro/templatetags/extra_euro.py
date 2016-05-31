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

def points(value, arg):
    if (value.filter(match__exact=arg).exists()):
        try :
            return value.get(match__exact=arg).points
        except (KeyError, Pronostic.DoesNotExist, RelatedObjectDoesNotExist ) :
            return -1
    else:   
        return None
    
    
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