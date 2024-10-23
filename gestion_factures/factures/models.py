from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='client')

    def __str__(self):
        return self.nom

class Facture(models.Model):
    titre = models.CharField(max_length=200, blank=False, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_emission = models.DateField(auto_now_add=True)
    date_paiement = models.DateField(null=True, blank=True)
    est_paye = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.titre} - {self.client.nom}"
