from django.contrib import admin
from .models import Conversation, ConversationMessage

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('item', 'created_at', 'modified_at')
    search_fields = ('item__name', 'members__username')
    list_filter = ('created_at', 'modified_at')
    filter_horizontal = ('members',)  # To make many-to-many field easier to manage

class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'content', 'created_at', 'created_by', 'is_read')
    search_fields = ('conversation__item__name', 'content', 'created_by__username')
    list_filter = ('created_at', 'is_read')

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationMessage, ConversationMessageAdmin)
