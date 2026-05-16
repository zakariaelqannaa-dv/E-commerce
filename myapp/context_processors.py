def selected_language(request):
    return {
        'selected_language': getattr(request, 'site_language', request.session.get('site_language', 'en')),
    }
