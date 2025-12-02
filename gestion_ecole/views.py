from django.shortcuts import render
# gestion_ec/views.py

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from import_eleves import importer_dernier_csv , Eleves # ou from gestion_ec.import_eleves import ...

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser, login_url='/admin/')
def refresh_eleves(request):
    importer_dernier_csv()
    messages.success(request, f"Liste des élèves mise à jour avec succès ! ({Eleves.objects.count()} élèves)")
    return redirect('/admin/')
def home(request):
    return render(request, 'home.html')
