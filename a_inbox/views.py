from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .forms import InboxNewMessageForm
from .models import *
from a_users.models import Profile


@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
    else:
        conversation = None
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations
    }
    return render(request, 'a_inbox/inbox.html', context)


def search_users(request):
    letters = request.GET.get('search_user')
    if len(letters) > 0:
        profiles = Profile.objects.filter(realname__icontains=letters).exclude(realname=request.user.profile.realname)
        users_ids = profiles.values_list('user', flat=True)
        users = User.objects.filter(
            Q(username__icontains=letters) | Q(id__in=users_ids)
        ).exclude(username=request.user.username)
        return render(request, 'a_inbox/list_searchuser.html', { 'users' : users })
    else:
        return HttpResponse('')
    
    
    
@login_required 
def new_message(request, recipient_id):
    recipient = get_object_or_404( User, id=recipient_id)
    new_message_form = InboxNewMessageForm()
    
    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            
            my_conversations = request.user.conversations.all()
            for conversation in my_conversations:
                if recipient in conversation.participants.all():
                    message.conversation = conversation
                    message.save()
                    conversation.lastmessage_created = timezone.now()
                    conversation.save()
                    return redirect('inbox', conversation.id) 
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, recipient)
            conversation.save()
            message.conversation = conversation
            message.save()
            return redirect('inbox', conversation.id)    
    
    context = {
        'recipient': recipient,
        'new_message_form': new_message_form
    }
    return render(request, 'a_inbox/form_newmessage.html', context)


@login_required
def new_reply(request, conversation_id):
    new_message_form = InboxNewMessageForm()
    my_conversations = request.user.conversations.all()
    conversation = get_object_or_404(my_conversations, id=conversation_id)
    
    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            conversation.lastmessage_created = timezone.now()
            conversation.save()
            message.save()
            return redirect('inbox', conversation.id)
    
    context = {
        'new_message_form': new_message_form,
        'conversation' : conversation
    }
    return render(request, 'a_inbox/form_newreply.html', context)
