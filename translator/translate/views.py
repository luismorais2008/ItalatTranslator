from django.shortcuts import render
from django.http import HttpResponse
import json 
import sys 


def index(request):
    if(request.method == "GET"): 
        try: 
            return HttpResponse("Get, with following body: " + str(request.body))
        except Exception: 
            print("little info")
            pass 
    return HttpResponse("Hello, world. You're at the polls index.")