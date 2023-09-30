from django.urls import path
from .views import *

urlpatterns = [
    path('', inbox_view, name="inbox"), 
    path('c/<conversation_id>/', inbox_view, name="inbox"), 
]
