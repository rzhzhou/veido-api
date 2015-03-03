from django.shortcuts import render
from django.http import HttpResponse

def index_view(request):
    return HttpResponse("hello world")

def category_view(request, ctg_id):
    return HttpResponse("category")

def location_view(request, location_id):
    return HttpResponse("location")
    
def person_view(request, person_id):
    return HttpResponse('person')
