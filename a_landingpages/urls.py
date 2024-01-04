from django.urls import path
from .views import *

urlpatterns = [
    path('maintenance/', maintenance_page, name="maintenance"),
    path('locked/', locked_page, name="locked"),
]