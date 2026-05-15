from django.contrib import admin
from .models import Prodotto, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descrizione')
    search_fields = ('nome',)


@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'quantita', 'prezzo', 'data_inserimento')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descrizione')
    date_hierarchy = 'data_inserimento'
    ordering = ('-data_inserimento',)
