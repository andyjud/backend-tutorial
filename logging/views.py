from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import user_passes_test

import logging
logger = logging.getLogger(__name__)

def home_view(request):
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    return render(request, 'home.html')


def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def view_log_file(request, filename):
    file_path = settings.BASE_DIR / filename
    if file_path.exists():
        with open(file_path, 'r') as file:
            response = HttpResponse(file.read(), content_type='text/plain')
            return response
    else:
        raise Http404("Log file does not exist")
