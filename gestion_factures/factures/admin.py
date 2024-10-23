from django.contrib import admin
from .models import Facture

def marquer_comme_paye(modeladmin, request, queryset):
    queryset.update(est_paye=True)
    
marquer_comme_paye.short_description = "Marquer les factures comme payées"

class FactureAdmin(admin.ModelAdmin):
    list_display = ('titre', 'client', 'montant', 'date_emission', 'est_paye')
    list_filter = ('client', 'est_paye')    
    search_fields = ('client__nom', 'titre')
    actions = [marquer_comme_paye]

admin.site.register(Facture, FactureAdmin)