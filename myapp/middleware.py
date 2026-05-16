from django.utils import translation

ALLOWED_SITE_LANGUAGES = ["en", "fr", "it", "es", "de"]
DEFAULT_SITE_LANGUAGE = "en"


class SiteLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = (
            request.session.get("site_language")
            or request.COOKIES.get("django_language")
            or DEFAULT_SITE_LANGUAGE
        )

        if lang not in ALLOWED_SITE_LANGUAGES:
            lang = DEFAULT_SITE_LANGUAGE

        request.site_language = lang
        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        response = self.get_response(request)
        response.set_cookie("django_language", lang)
        translation.deactivate()
        return response
