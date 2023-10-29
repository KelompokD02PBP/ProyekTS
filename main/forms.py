from django import forms
from .models import ProfileUser, Comment

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields=['email', 'profile_picture', 'address']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']