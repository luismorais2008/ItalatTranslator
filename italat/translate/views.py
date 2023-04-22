"""from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def main(request):
    return HttpResponse("Hello, world. You're at the polls index. Autoupdate?")
"""
from django.http import HttpResponse
from django.shortcuts import render

from .forms import NameForm

def main(request):
    #form = NameForm()

    return HttpResponse('hey')