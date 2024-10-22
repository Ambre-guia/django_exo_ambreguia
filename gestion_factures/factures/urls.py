from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.facture_list, name='facture_list'),
    path('create/', views.facture_create, name='facture_create'),
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
    path('<int:pk>/edit/', views.facture_update, name='facture_update'),
    path('<int:pk>/delete/', views.facture_delete, name='facture_delete'),

    path('clients/create/', views.client_create, name='client_create'), 
    path('categories/create/', views.categorie_create, name='categorie_create'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('signup/', views.signup, name='signup'),
    ]
