import os
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from .models import Prodotto, Categoria


def set_language(request, lang):
    allowed = ['en', 'fr', 'it', 'es', 'de']
    if lang in allowed:
        request.session['site_language'] = lang
        translation.activate(lang)
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('django_language', lang)
    return response


def is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

admin_required = user_passes_test(is_admin_user, login_url="/")


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


MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def _validate_image(uploaded_file):
    """Validate uploaded image file size and extension. Returns error message or None."""
    if not uploaded_file:
        return None
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return _('Formato immagine non supportato. Usa JPG, PNG, GIF o WEBP.')
    if uploaded_file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        return _(f'L\'immagine non può superare i {MAX_IMAGE_SIZE_MB}MB.')
    return None


def _validate_product_data(nome, descrizione, quantita, prezzo, categoria_id):
    """Validate product input data, returning (cleaned_data, error_message)."""
    if not all([nome, descrizione, quantita, prezzo]):
        return None, _('Tutti i campi obbligatori devono essere compilati.')
    try:
        quantita_int = int(quantita)
        if quantita_int < 0:
            return None, _('La quantità deve essere un numero positivo.')
    except (ValueError, TypeError):
        return None, _('La quantità deve essere un numero valido.')
    try:
        prezzo_dec = Decimal(prezzo)
        if prezzo_dec < 0:
            return None, _('Il prezzo deve essere un numero positivo.')
    except (InvalidOperation, TypeError):
        return None, _('Il prezzo deve essere un numero valido.')
    categoria = None
    if categoria_id:
        try:
            categoria = Categoria.objects.get(id=categoria_id)
        except (ValueError, Categoria.DoesNotExist):
            return None, _('Categoria non valida.')
    return {'quantita': quantita_int, 'prezzo': prezzo_dec, 'categoria': categoria}, None


@admin_required
def form_prodotti(request):
    categorie = Categoria.objects.all()
    prodotti_count = Prodotto.objects.count()
    context = {'categorie': categorie, 'prodotti_count': prodotti_count}

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descrizione = request.POST.get('descrizione', '').strip()
        quantita = request.POST.get('quantita', '').strip()
        prezzo = request.POST.get('prezzo', '').strip()
        categoria_id = request.POST.get('categoria', '').strip()
        immagine = request.FILES.get('immagine')

        cleaned, error = _validate_product_data(nome or 'tmp', descrizione or 'tmp', quantita, prezzo, categoria_id)
        if error:
            messages.error(request, error)
            return render(request, 'myapp/form_prodotti.html', context)

        img_error = _validate_image(immagine)
        if img_error:
            messages.error(request, img_error)
            return render(request, 'myapp/form_prodotti.html', context)

        # Collect translation fields
        lang_fields = {}
        for lang in ['en', 'fr', 'it', 'es', 'de']:
            n = request.POST.get(f'nome_{lang}', '').strip()
            d = request.POST.get(f'descrizione_{lang}', '').strip()
            lang_fields[f'nome_{lang}'] = n or None
            lang_fields[f'descrizione_{lang}'] = d or None

        # Determine fallback nome/descrizione from first non-empty translation
        fallback_name = nome or lang_fields.get('nome_en') or lang_fields.get('nome_it') or lang_fields.get('nome_fr') or lang_fields.get('nome_es') or lang_fields.get('nome_de') or ''
        fallback_desc = descrizione or lang_fields.get('descrizione_en') or lang_fields.get('descrizione_it') or lang_fields.get('descrizione_fr') or lang_fields.get('descrizione_es') or lang_fields.get('descrizione_de') or ''

        if not fallback_name or not fallback_desc:
            messages.error(request, _('Tutti i campi obbligatori devono essere compilati.'))
            return render(request, 'myapp/form_prodotti.html', context)

        # Copy to _en if not provided
        if not lang_fields.get('nome_en'):
            lang_fields['nome_en'] = fallback_name
        if not lang_fields.get('descrizione_en'):
            lang_fields['descrizione_en'] = fallback_desc

        try:
            Prodotto.objects.create(
                nome=fallback_name,
                descrizione=fallback_desc,
                quantita=cleaned['quantita'],
                prezzo=cleaned['prezzo'],
                categoria=cleaned['categoria'],
                immagine=immagine,
                **lang_fields,
            )
            messages.success(request, f'{_("Prodotto")} "{fallback_name}" {_("aggiunto con successo.")}')
            return redirect('lista_prodotti')
        except Exception:
            messages.error(request, _('Errore durante il salvataggio. Riprova più tardi.'))

    return render(request, 'myapp/form_prodotti.html', context)


def lista_prodotti(request):
    if request.method == 'POST':
        if not request.user.is_staff and not request.user.is_superuser:
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
            Q(nome_en__icontains=query) |
            Q(nome_fr__icontains=query) |
            Q(nome_it__icontains=query) |
            Q(nome_es__icontains=query) |
            Q(nome_de__icontains=query) |
            Q(descrizione_en__icontains=query) |
            Q(descrizione_fr__icontains=query) |
            Q(descrizione_it__icontains=query) |
            Q(descrizione_es__icontains=query) |
            Q(descrizione_de__icontains=query) |
            Q(categoria__nome__icontains=query)
        )
    categorie = Categoria.objects.all()
    return render(request, 'myapp/lista_prodotti.html', {
        'prodotti': prodotti,
        'categorie': categorie,
        'query': query,
    })


@admin_required
def gestione_categorie(request):
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


@admin_required
@require_POST
def aggiungi_categoria_rapida(request):
    """Quick category creation from the product entry page modal."""
    nome = request.POST.get('nome', '').strip()
    descrizione = request.POST.get('descrizione', '').strip()
    if not nome:
        messages.error(request, _('Il nome della categoria è obbligatorio.'))
    elif Categoria.objects.filter(nome__iexact=nome).exists():
        messages.error(request, _('Categoria "%(nome)s" già esistente.') % {'nome': nome})
    else:
        Categoria.objects.create(nome=nome, descrizione=descrizione)
        messages.success(request, _('Categoria "%(nome)s" creata.') % {'nome': nome})
    return redirect('form_prodotti')


@admin_required
def modifica_prodotto(request, prodotto_id):
    prodotto = get_object_or_404(Prodotto, id=prodotto_id)
    categorie = Categoria.objects.all()

    if request.method == 'POST':
        nome = request.POST.get('nome', prodotto.nome).strip()
        descrizione = request.POST.get('descrizione', prodotto.descrizione).strip()
        quantita = request.POST.get('quantita', str(prodotto.quantita)).strip()
        prezzo = request.POST.get('prezzo', str(prodotto.prezzo)).strip()
        categoria_id = request.POST.get('categoria', '').strip()

        cleaned, error = _validate_product_data(nome or 'tmp', descrizione or 'tmp', quantita, prezzo, categoria_id)
        if error:
            messages.error(request, error)
            return render(request, 'myapp/form_prodotti.html', {
                'prodotto': prodotto,
                'categorie': categorie,
            })

        immagine = request.FILES.get('immagine')
        img_error = _validate_image(immagine)
        if img_error:
            messages.error(request, img_error)
            return render(request, 'myapp/form_prodotti.html', {
                'prodotto': prodotto,
                'categorie': categorie,
            })

        # Collect translation fields
        for lang in ['en', 'fr', 'it', 'es', 'de']:
            n = request.POST.get(f'nome_{lang}', '').strip()
            d = request.POST.get(f'descrizione_{lang}', '').strip()
            setattr(prodotto, f'nome_{lang}', n or None)
            setattr(prodotto, f'descrizione_{lang}', d or None)

        # Determine fallback
        fallback_name = (nome or prodotto.nome_en or prodotto.nome_it or prodotto.nome_fr or prodotto.nome_es or prodotto.nome_de or '')
        fallback_desc = (descrizione or prodotto.descrizione_en or prodotto.descrizione_it or prodotto.descrizione_fr or prodotto.descrizione_es or prodotto.descrizione_de or '')
        if not fallback_name or not fallback_desc:
            messages.error(request, _('Tutti i campi obbligatori devono essere compilati.'))
            return render(request, 'myapp/form_prodotti.html', {'prodotto': prodotto, 'categorie': categorie})

        prodotto.nome = fallback_name
        prodotto.descrizione = fallback_desc
        if not prodotto.nome_en:
            prodotto.nome_en = fallback_name
        if not prodotto.descrizione_en:
            prodotto.descrizione_en = fallback_desc
        prodotto.quantita = cleaned['quantita']
        prodotto.prezzo = cleaned['prezzo']
        prodotto.categoria = cleaned['categoria']
        if immagine:
            prodotto.immagine = immagine
        prodotto.save()
        messages.success(request, f'{_("Prodotto")} "{prodotto.nome}" {_("aggiornato.")}')
        return redirect('lista_prodotti')

    return render(request, 'myapp/form_prodotti.html', {
        'prodotto': prodotto,
        'categorie': categorie,
    })
