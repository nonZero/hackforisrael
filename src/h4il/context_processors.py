from django.conf import settings


def hackita_processor(request):
    return {
            'PRODUCTION': not settings.DEBUG
           }
