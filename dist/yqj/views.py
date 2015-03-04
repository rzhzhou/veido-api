from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def index_view(request):
    return render_to_response("dashboard/dashboard.html")

def category_view(request, ctg_id):
    return render_to_response('category/category.html')

def location_view(request, location_id):
    return render_to_response("location/location.html")
    
def person_view(request, person_id):
    return HttpResponse('person')

def login_view(request):
    return render_to_response('user/login.html')
