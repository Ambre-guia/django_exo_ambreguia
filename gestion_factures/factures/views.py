from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Facture, Categorie, Client
from .forms import FactureForm
from .forms import ClientForm
from .forms import CategorieForm

from django.contrib.auth.models import User
from .forms import SignUpForm, UserForm
from django.core.exceptions import PermissionDenied
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


##################
## Facture app ###
##################
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

##################
## User gestion ##
##################
@login_required
def user_list(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    users = User.objects.all()
    return render(request, 'factures/user_list.html', {'users': users})

@login_required
def user_create(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'factures/user_form.html', {'form': form})

@login_required
def user_update(request, user_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'factures/user_form.html', {'form': form})

@login_required
def user_delete(request, user_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('user_list')
    return render(request, 'factures/user_confirm_delete.html', {'user': user})