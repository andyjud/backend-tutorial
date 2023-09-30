from django.contrib import admin

from .models import *

admin.site.register(InboxMessage)
admin.site.register(Conversation)
