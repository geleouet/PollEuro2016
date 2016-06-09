from django.contrib import admin

# Register your models here.

from .models import Pays, Rencontre, Member, Pronostic, Tag, Resultat, Team, MatchPool, PollChoices

admin.site.register(Pays)
admin.site.register(Tag)
admin.site.register(Rencontre)
admin.site.register(Member)
admin.site.register(Pronostic)
admin.site.register(Resultat)
admin.site.register(Team)
admin.site.register(MatchPool)
admin.site.register(PollChoices)

