from django import forms
from django.forms import ModelForm
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

