from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='client')
    country = CountryField(default='FR')  

    def __str__(self):
        return self.nom

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.percentage}%"

class Facture(models.Model):
    titre = models.CharField(max_length=200, blank=False, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_emission = models.DateField(auto_now_add=True)
    date_paiement = models.DateField(null=True, blank=True)
    est_paye = models.BooleanField(default=False)
    discounts = models.ManyToManyField(Discount, blank=True) 

    def get_subtotal(self):
        return sum(article.get_subtotal() for article in self.articles.all())
    
    def get_tax_rate(self):
        tax = Tax.objects.filter(country=self.client.country).first()
        if tax:
            return tax.rate
        return 0
    
    def get_total(self):
        subtotal = self.get_subtotal()

        for discount in self.discounts.filter(is_active=True):
            discount_value = (discount.percentage / 100) * subtotal
            subtotal -= discount_value

        tax_rate = self.get_tax_rate()
        total = subtotal + (tax_rate * subtotal / 100)

        return total
    
    def __str__(self):
        return f"{self.titre} - {self.client.nom}"
    
    def clean(self):
        if not self.articles.exists():
            raise ValidationError("Une facture doit avoir au moins un article.")

    


class Article(models.Model):
    description = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    facture = models.ForeignKey('Facture', related_name='articles', on_delete=models.CASCADE)

    def get_subtotal(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.unit_price}"
    

    
class Tax(models.Model):
    country = CountryField() 
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.country} - {self.rate}%"