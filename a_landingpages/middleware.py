from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .models import LandingPage

def landingpage_middleware(get_response):
    def middleware(request):

        if page_is_enabled('Maintenance'):
            if request.path != reverse('maintenance'):
                if '/theboss' not in request.path:
                    if settings.STAGING != 'True':
                        return HttpResponseRedirect(reverse('maintenance'))
                    
        if page_is_enabled('Staging'):
            if request.path != reverse('locked'):
                if '/theboss' not in request.path:
                    if settings.STAGING == 'True':
                        if 'staging_access' not in request.session:
                            return HttpResponseRedirect(reverse('locked'))
        
        response = get_response(request)
        return response
    
    return middleware


def page_is_enabled(page_name):
    page = LandingPage.objects.filter(name=page_name).first()
    if page:
        return page.is_enabled
    else:
        return False