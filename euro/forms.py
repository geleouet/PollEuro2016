from django import forms
from .models import Member, Team

class memberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['team']
        team = forms.ModelChoiceField(queryset=Team.objects.all())

    def save(self, request):

        data = request.POST
        print "Printing Data",len(data['team'])
        user =request.user.member
        team = Team(pk=data['team'])
        if team is None:
            print "Pas d'equip"
        user.team = team
        user.save()


class creatTeam(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']

    def creatTeam(self):
        pass