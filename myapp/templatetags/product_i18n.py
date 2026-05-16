from django import template

register = template.Library()

ALLOWED_LANGUAGES = ['en', 'fr', 'it', 'es', 'de']


@register.filter
def translated_name(product, lang):
    if lang not in ALLOWED_LANGUAGES:
        lang = 'en'
    value = getattr(product, f'nome_{lang}', None)
    return value or getattr(product, 'nome_en', None) or getattr(product, 'nome', '')


@register.filter
def translated_description(product, lang):
    if lang not in ALLOWED_LANGUAGES:
        lang = 'en'
    value = getattr(product, f'descrizione_{lang}', None)
    return value or getattr(product, 'descrizione_en', None) or getattr(product, 'descrizione', '')
