from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Facture, Categorie, Client
from .forms import FactureForm
from .forms import ClientForm
from .forms import CategorieForm

from django.contrib.auth.models import User
from .forms import SignUpForm
from factures.decorators import superuser_required

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False 
            user.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def facture_list(request):

    clients = Client.objects.all()
    client_id = request.GET.get('client_id')
    if client_id:
        factures = Facture.objects.filter(client_id=client_id)
    else:
        factures = Facture.objects.all()
    
    context = {
            'factures': factures,
            'clients': clients,  
        }
    return render(request, 'factures/facture_list.html', context)

@login_required
@superuser_required
def facture_create(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save(commit=False)
            if not facture.categorie:
                categorie_autres, created = Categorie.objects.get_or_create(nom="Autres")
                facture.categorie = categorie_autres
            facture.save()
            return redirect('facture_list')
    else:
        form = FactureForm()
    return render(request, 'factures/facture_form.html', {'form': form})

@login_required
@superuser_required
def facture_update(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            return redirect('facture_list')
    else:
        form = FactureForm(instance=facture)
    return render(request, 'factures/facture_form.html', {'form': form})

@login_required
@superuser_required
def facture_delete(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        facture.delete()
        return redirect('facture_list')
    return render(request, 'factures/facture_confirm_delete.html', {'facture': facture})


@login_required
def facture_detail(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'factures/facture_detail.html', {'facture': facture})

@login_required
@superuser_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_create') 
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})

@login_required
@superuser_required
def categorie_create(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_create') 
    else:
        form = CategorieForm()
    return render(request, 'categories/categorie_form.html', {'form': form})