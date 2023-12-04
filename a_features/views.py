from django.shortcuts import render
from django.conf import settings
from .models import Feature

def feature_enabled(id, developer):
    feature = Feature.objects.get(id=id)
    
    if (settings.ENVIRONMENT == 'development' and settings.DEVELOPER == developer) or \
        (feature.staging_enabled and settings.STAGING == 'True') or \
        feature.production_enabled:
        feature_enabled = True
    else:
        feature_enabled = False
        
    return feature_enabled
