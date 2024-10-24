from django import forms
from .models import Facture, Client, Categorie, Tax, Article

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import inlineformset_factory


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff'] 

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['titre', 'client', 'categorie', 'montant', 'date_paiement', 'est_paye', 'discounts']

        widgets = {
                    'date_paiement': forms.DateInput(attrs={'type': 'date'}),
                }
    
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=True, empty_label="Sélectionner un client")
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), required=False, empty_label="Sélectionner une catégorie")

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        
        if not Client.objects.exists():
            self.fields['client'].empty_label = "Créer un nouveau client"
        if not Categorie.objects.exists():
            self.fields['categorie'].empty_label = "Créer une nouvelle catégorie"

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'email', 'country']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
        }

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_superuser', 'is_staff']
        widgets = {
            'password': forms.PasswordInput(),
        }

class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['country', 'rate']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['description', 'unit_price', 'quantity']

ArticleFormSet = inlineformset_factory(Facture, Article, form=ArticleForm, extra=1, can_delete=True)