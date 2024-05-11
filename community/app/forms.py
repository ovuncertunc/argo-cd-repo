from django import forms
from .models import Community, Posts, UserProfile, UserCommunityMembership

class CommunityCreationForm(forms.ModelForm):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    privacy = forms.ChoiceField(choices=PRIVACY_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Community
        fields = ['name', 'privacy', 'description', "community_photo"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content', 'event_date']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "birthdate", "about_me", "profile_picture")
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'})
        }