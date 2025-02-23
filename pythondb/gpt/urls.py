from django.urls import path
from .views import chat, clean_chat

app_name = "gpt"


urlpatterns = [
    path('', chat, name='chat'),
    path('clean-chat/', clean_chat, name='clean_chat'),

]