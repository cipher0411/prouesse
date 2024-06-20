# # api_views.py

# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import ConversationMessage

# @login_required
# def unread_messages_count(request):
#     unread_count = ConversationMessage.objects.filter(conversation__members=request.user, is_read=False).exclude(created_by=request.user).count()
#     return JsonResponse({'unread_count': unread_count})