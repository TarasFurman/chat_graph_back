from core import consumers
from django.urls import path


websocket_urlpatterns = [
    path("ws/chat_room/<int:chat_id>", consumers.ChatConsumer, name="chat_room",),
]
