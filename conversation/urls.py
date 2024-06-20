from django.urls import path
from . import views #api_views  # Import api_views here

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),  
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
    #  path('unread-messages-count/', views.unread_messages_count, name='unread_messages_count'),
    
]
