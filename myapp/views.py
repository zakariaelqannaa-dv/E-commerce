from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils.translation import gettext as _
from .models import Prodotto, Categoria

ACCESS_CODE = '2005zakaria'


def dettaglio_prodotto(request, prodotto_id):
    prodotto = get_object_or_404(Prodotto.objects.select_related('categoria'), id=prodotto_id)
    related = Prodotto.objects.select_related('categoria').filter(categoria=prodotto.categoria).exclude(id=prodotto.id)[:4] if prodotto.categoria else []
    return render(request, 'myapp/dettaglio_prodotto.html', {'prodotto': prodotto, 'related_products': related})


def home(request):
    ultimi_prodotti = Prodotto.objects.select_related('categoria').order_by('-data_inserimento')[:8]
    context = {
        'ultimi_prodotti': ultimi_prodotti,
        'prodotti_count': Prodotto.objects.count(),
        'categorie_count': Categoria.objects.count(),
    }
    return render(request, 'myapp/home.html', context)


def contatti(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        cognome = request.POST.get('cognome', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        oggetto = request.POST.get('oggetto', '').strip()
        messaggio = request.POST.get('messaggio', '').strip()

        if not all([nome, cognome, email, oggetto, messaggio]):
            messages.error(request, _('Tutti i campi obbligatori devono essere compilati.'))
        else:
            messages.success(request, _('Grazie %(nome)s, il tuo messaggio è stato inviato. Ti risponderemo entro 24 ore.') % {'nome': nome})
            return redirect('contatti')

    return render(request, 'myapp/contatti.html')


def form_prodotti(request):
    # Handle access code submission
    if request.method == 'POST' and 'access_code' in request.POST:
        code = request.POST.get('access_code', '').strip()
        if code == ACCESS_CODE:
            request.session['can_add_product'] = True
            messages.success(request, _('Accesso autorizzato.'))
            return redirect('form_prodotti')
        else:
            messages.error(request, _('Codice di accesso non valido.'))
            return redirect('form_prodotti')

    can_add = request.session.get('can_add_product', False)

    if not can_add:
        return render(request, 'myapp/form_prodotti.html', {'show_code_form': True})

    categorie = Categoria.objects.all()
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descrizione = request.POST.get('descrizione', '').strip()
        quantita = request.POST.get('quantita', '').strip()
        prezzo = request.POST.get('prezzo', '').strip()
        categoria_id = request.POST.get('categoria', '').strip()
        immagine = request.FILES.get('immagine')

        if not all([nome, descrizione, quantita, prezzo]):
            messages.error(request, _('Tutti i campi obbligatori devono essere compilati.'))
            return render(request, 'myapp/form_prodotti.html', {'categorie': categorie})

        try:
            categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
            quantita_int = int(quantita)
            prezzo_dec = Decimal(prezzo)
            Prodotto.objects.create(
                nome=nome,
                descrizione=descrizione,
                quantita=quantita_int,
                prezzo=prezzo_dec,
                categoria=categoria,
                immagine=immagine,
            )
            messages.success(request, f'{_("Prodotto")} "{nome}" {_("aggiunto con successo.")}')
            return redirect('lista_prodotti')
        except Exception as e:
            messages.error(request, f'{_("Errore durante il salvataggio:")} {e}')

    return render(request, 'myapp/form_prodotti.html', {'categorie': categorie})


def lista_prodotti(request):
    if request.method == 'POST':
        can_add = request.session.get('can_add_product', False)
        if not can_add:
            messages.error(request, _('Non autorizzato.'))
            return redirect('lista_prodotti')

        prodotto_id = request.POST.get('prodotto_id')
        if prodotto_id:
            try:
                prodotto = Prodotto.objects.get(id=prodotto_id)
                nome = prodotto.nome
                prodotto.delete()
                messages.success(request, f'{_("Prodotto")} "{nome}" {_("eliminato.")}')
            except Prodotto.DoesNotExist:
                messages.error(request, _('Prodotto non trovato.'))
            return redirect('lista_prodotti')

        ids = request.POST.getlist('prodotti_da_cancellare')
        if ids:
            deleted_count, _ = Prodotto.objects.filter(id__in=ids).delete()
            if deleted_count == 1:
                messages.success(request, f'{deleted_count} {_("prodotto")} {_("eliminato")}.')
            else:
                messages.success(request, f'{deleted_count} {_("prodotti")} {_("eliminati")}.')
        return redirect('lista_prodotti')

    query = request.GET.get('q', '').strip()
    prodotti = Prodotto.objects.select_related('categoria').order_by('-data_inserimento')
    if query:
        prodotti = prodotti.filter(
            Q(nome__icontains=query) |
            Q(descrizione__icontains=query) |
            Q(categoria__nome__icontains=query)
        )
    categorie = Categoria.objects.all()
    return render(request, 'myapp/lista_prodotti.html', {
        'prodotti': prodotti,
        'categorie': categorie,
        'query': query,
    })


def gestione_categorie(request):
    can_add = request.session.get('can_add_product', False)
    if not can_add:
        return redirect('form_prodotti')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descrizione = request.POST.get('descrizione', '').strip()
        if nome:
            Categoria.objects.create(nome=nome, descrizione=descrizione)
            messages.success(request, _('Categoria "%(nome)s" creata.') % {'nome': nome})
        else:
            messages.error(request, _('Il nome della categoria è obbligatorio.'))
        return redirect('gestione_categorie')

    categorie = Categoria.objects.all()
    return render(request, 'myapp/gestione_categorie.html', {'categorie': categorie})


def esci_admin(request):
    request.session.pop('can_add_product', None)
    messages.success(request, _('Modalità amministratore disattivata.'))
    return redirect('home')


def modifica_prodotto(request, prodotto_id):
    can_add = request.session.get('can_add_product', False)
    if not can_add:
        messages.error(request, _('Devi prima autorizzarti per modificare prodotti.'))
        return redirect('form_prodotti')

    prodotto = get_object_or_404(Prodotto, id=prodotto_id)
    categorie = Categoria.objects.all()

    if request.method == 'POST':
        prodotto.nome = request.POST.get('nome', prodotto.nome).strip()
        prodotto.descrizione = request.POST.get('descrizione', prodotto.descrizione).strip()
        prodotto.quantita = int(request.POST.get('quantita', prodotto.quantita))
        prodotto.prezzo = Decimal(request.POST.get('prezzo', str(prodotto.prezzo)))
        categoria_id = request.POST.get('categoria', '')
        prodotto.categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
        if request.FILES.get('immagine'):
            prodotto.immagine = request.FILES.get('immagine')
        prodotto.save()
        messages.success(request, f'{_("Prodotto")} "{prodotto.nome}" {_("aggiornato.")}')
        return redirect('lista_prodotti')

    return render(request, 'myapp/form_prodotti.html', {
        'prodotto': prodotto,
        'categorie': categorie,
    })
