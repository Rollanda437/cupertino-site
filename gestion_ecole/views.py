from django.shortcuts import render
# gestion_ec/views.py
def home(request):
    return render(request, 'home.html')
