from django.test import TestCase, Client as TestClient
from .models import Facture, Client, Categorie
from django.urls import reverse
from django.contrib.auth.models import User

##########################
## Test facture  model ###
##########################
class FactureModelTest(TestCase):
    
    def setUp(self):
        self.client = Client.objects.create(nom="Client Test")
        self.categorie = Categorie.objects.create(nom="Catégorie Test")

    def test_facture_creation(self):
        facture = Facture.objects.create(
            titre="Facture 1",
            client=self.client,
            categorie=self.categorie,
            montant=100.00,
            date_paiement="2024-10-10",
            est_paye=False
        )
        self.assertEqual(facture.titre, "Facture 1")
        self.assertEqual(facture.client, self.client)
        self.assertEqual(facture.categorie, self.categorie)
        self.assertEqual(facture.montant, 100.00)
        self.assertFalse(facture.est_paye)

    def test_facture_str(self):
        facture = Facture.objects.create(
            titre="Facture 2",
            client=self.client,
            categorie=self.categorie,
            montant=150.00,
            date_paiement="2024-10-15",
            est_paye=True
        )
        self.assertEqual(str(facture), "Facture 2 - Client Test")

    def test_facture_paiement(self):
        facture = Facture.objects.create(
            titre="Facture 3",
            client=self.client,
            categorie=self.categorie,
            montant=200.00,
            date_paiement="2024-10-20",
            est_paye=False
        )
        facture.est_paye = True
        facture.save()
        self.assertTrue(facture.est_paye)

############################
## Test facture vue list ###
############################
class FactureViewsTest(TestCase):

    def setUp(self):
        
        self.test_client = TestClient() 
        self.client_instance = Client.objects.create(nom="Client Test")
        self.categorie = Categorie.objects.create(nom="Catégorie Test")
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.facture = Facture.objects.create(
            titre="Facture 1",
            client=self.client_instance,
            categorie=self.categorie,
            montant=100.00,
            date_paiement="2024-10-10",
            est_paye=False
        )

    def test_list_factures_view(self):
        self.test_client.login(username='testuser', password='testpass') 
        response = self.test_client.get(reverse('facture_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/facture_list.html')
        self.assertContains(response, "Facture 1")
    
    def test_list_factures_view_empty(self):

        self.test_client.login(username='testuser', password='testpass')
        self.facture.delete()  
        
        response = self.test_client.get(reverse('facture_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'factures/facture_list.html')
        self.assertContains(response, "Aucune facture trouvée")

    def test_list_factures_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('facture_list'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, f"/accounts/login/?next={reverse('facture_list')}")

##############################
## Test facture vue detail ###
##############################

class FactureDetailViewTest(TestCase):

    def setUp(self):
        self.test_client = TestClient() 
        self.client_instance = Client.objects.create(nom="Client Test") 
        self.categorie = Categorie.objects.create(nom="Catégorie Test")
        self.facture = Facture.objects.create(
            titre="Facture 1",
            client=self.client_instance, 
            categorie=self.categorie,
            description="facture 1 test",
            montant=100.0,
            date_paiement="2024-10-10",
            est_paye=False
        )
        self.user = User.objects.create_user(username='testuser', password='testpass') 

    def test_facture_detail_view(self):
        self.test_client.login(username='testuser', password='testpass') 
        response = self.test_client.get(reverse('facture_detail', args=[self.facture.id]))
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Facture 1")
        self.assertContains(response, "Client Test")

    def test_facture_detail_view_not_authenticated(self):
        self.test_client.logout()  
        response = self.test_client.get(reverse('facture_detail', args=[self.facture.id]))
        self.assertEqual(response.status_code,302)  
        self.assertRedirects(response, f'/accounts/login/?next=/factures/{self.facture.id}/')

    def test_facture_detail_view_not_found(self):
        self.test_client.login(username='testuser', password='testpass')
        response = self.test_client.get(reverse('facture_detail', args=[999]))  
        self.assertEqual(response.status_code, 404)

##############################
## Test facture vue create ###
##############################

class FactureCreateViewTest(TestCase):

    def setUp(self):
        self.client_instance = Client.objects.create(nom="Client Test")
        self.categorie = Categorie.objects.create(nom="Catégorie Test")
        self.user = User.objects.create_superuser(username='testuser', password='testpass')
    
    def test_create_facture_view(self):
        self.client.login(username='testuser', password='testpass') 
        response = self.client.post(reverse('facture_create'), {
            'titre': 'Facture Test',
            'client': self.client_instance.id, 
            'categorie': self.categorie.id,
            'montant': 150.00,
            'date_paiement': '2024-10-20',
            'est_paye': False
        }) 
        if response.context and 'form' in response.context:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 200)  
        self.assertFalse(Facture.objects.filter(titre='Facture Test').exists())

    def test_create_facture_view_not_authenticated(self):
        response = self.client.get(reverse('facture_create'))
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, '/accounts/login/?next=/factures/create/')

    def test_create_facture_view_invalid_data(self):
        self.client.login(username='testuser', password='testpass') 
        response = self.client.post(reverse('facture_create'), {
            'titre': '', 
            'client': self.client_instance.id,
            'categorie': self.categorie.id,
            'montant': 150.00,
            'date_paiement': '2024-10-20',
            'est_paye': False
        })
        self.assertEqual(response.status_code, 200) 
        form = response.context['form']
        self.assertFormError(form, 'titre', 'This field is required.')
