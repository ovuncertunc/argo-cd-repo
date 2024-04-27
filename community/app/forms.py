from django import forms
from .models import Community, DefaultTemplate, UserCommunityMembership

class CommunityCreationForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'privacy']

class DefaultTemplateForm(forms.ModelForm):
    class Meta:
        model = DefaultTemplate
        fields = ['title', 'content', 'event_date']