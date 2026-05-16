from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('language/<str:lang>/', views.set_language, name='set_language'),
    path('prodotti/', views.lista_prodotti, name='lista_prodotti'),
    path('prodotti/<int:prodotto_id>/', views.dettaglio_prodotto, name='dettaglio_prodotto'),
    path('prodotti/nuovo/', views.form_prodotti, name='form_prodotti'),
    path('prodotti/modifica/<int:prodotto_id>/', views.modifica_prodotto, name='modifica_prodotto'),
    path('categorie/', views.gestione_categorie, name='gestione_categorie'),
    path('categorie/aggiungi-rapida/', views.aggiungi_categoria_rapida, name='aggiungi_categoria_rapida'),
    path('contatti/', views.contatti, name='contatti'),
]
