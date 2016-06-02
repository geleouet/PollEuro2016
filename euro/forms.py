from django import forms
from .models import Member, Team

class memberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['team']
        team = forms.ModelChoiceField(queryset=Team.objects.all())

# class teamCreationFrom(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ['name', 'description']
