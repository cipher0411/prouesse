# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from item.models import Category, Item

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    
    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])
    
    if conversations.exists():
        return redirect('conversation:detail', pk=conversations.first().pk)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
        
    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    # unread_count = ConversationMessage.objects.filter(conversation__members=request.user, is_read=False).exclude(created_by=request.user).count()
        
    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
        # 'unread_count': unread_count
    })

@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)
    
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    # Mark all messages as read when the user views the conversation
    # conversation.messages.filter(is_read=False).exclude(created_by=request.user).update(is_read=True)
    
    # return render(request, 'conversation/detail.html', {
    #     'conversation': conversation,
    #     'form': form
    # })

# Unread messages count
# @login_required
# def unread_messages_count(request):
#     unread_count = ConversationMessage.objects.filter(conversation__members=request.user, is_read=False).exclude(created_by=request.user).count()
#     return unread_count

# Home page view
# def index(request):
#     items = Item.objects.filter(is_sold=False).order_by('-created_at')[:6]
#     categories = Category.objects.all()
#     unread_count = unread_messages_count(request)
#     return render(request, 'core/index.html', {
#         'categories': categories,
#         'items': items,
#         'unread_count': unread_count,
#     })

