from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timesince import timesince
from cryptography.fernet import Fernet
from django.conf import settings
import uuid


class InboxMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name="messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def body_decrypted(self):
        f = Fernet(settings.ENCRYPT_KEY)
        message_decrypted = f.decrypt(self.body)
        message_decoded = message_decrypted.decode('utf-8')
        return message_decoded
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f'[{self.sender.username} : {time_since} ago]'
    
    
class Conversation(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-lastmessage_created']
        
    def __str__(self):
        user_names = ", ".join(user.username for user in self.participants.all())
        return f'[{user_names}]'
