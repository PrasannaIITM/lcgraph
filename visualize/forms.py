from django.forms import ModelForm
from django import forms
from .models import username

class Form(forms.Form):
    username = forms.CharField()

