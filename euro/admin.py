from django.contrib import admin

# Register your models here.

from .models import Pays, Rencontre, Member

admin.site.register(Pays)
admin.site.register(Rencontre)
admin.site.register(Member)