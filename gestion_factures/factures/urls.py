from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import user_list, user_create, user_update, user_delete, client_list,article_list, article_delete, article_update, article_create,  categorie_list

urlpatterns = [
    path('', views.facture_list, name='facture_list'),
    path('create/', views.facture_create, name='facture_create'),
    path('<int:pk>/', views.facture_detail, name='facture_detail'),
    path('<int:pk>/edit/', views.facture_update, name='facture_update'),
    path('<int:pk>/delete/', views.facture_delete, name='facture_delete'),

    path('clients/', client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'), 
    
    path('categories/', categorie_list, name='categories_list'),
    path('categories/create/', views.categorie_create, name='categorie_create'),

    path('articles/', article_list, name='article_list'),
    path('articles/create/', article_create, name='article_create'),
    path('articles/<int:article_id>/update/', article_update, name='article_update'),
    path('articles/<int:article_id>/delete/', article_delete, name='article_delete'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('signup/', views.signup, name='signup'),

    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:user_id>/update/', user_update, name='user_update'),
    path('users/<int:user_id>/delete/', user_delete, name='user_delete'),

    path('taxes/', views.tax_list, name='tax_list'),
    path('taxes/create/', views.create_tax, name='create_tax'),
    path('taxes/<int:tax_id>/edit/', views.edit_tax, name='edit_tax'),
    path('taxes/<int:tax_id>/delete/', views.delete_tax, name='delete_tax'),
    ]
