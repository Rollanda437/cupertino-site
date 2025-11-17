from django.shortcuts import render
from django.http import HttpResponse

def index_calendrier(request):
    return render(request, "calendrier.html")

# Create your views here.
