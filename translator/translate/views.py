from django.shortcuts import render
from django.http import HttpResponse
import json 
import sys 
from translate import texto_portuguese_to_italat


def index(request):
    if(request.method == "GET"): 
        try: 
            return HttpResponse(texto_portuguese_to_italat(request.body))
        except Exception: 
            pass 
    return HttpResponse("Sorry, something went wrong. Try again in a few ages.")